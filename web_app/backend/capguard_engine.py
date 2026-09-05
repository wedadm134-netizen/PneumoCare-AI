from __future__ import annotations

from typing import Any, Dict, Optional


ENGINE_VERSION = "CAPGuard Production Engine V1"

# ============================================================
# LOCKED EVIDENCE-FUSE V4
# ============================================================

V4_NLP_WEIGHT = 0.73
V4_VITAL_WEIGHT = 0.27
V4_THRESHOLD = 0.665


# ============================================================
# LOCKED CBC V5
# ============================================================

CBC_V5_V4_WEIGHT = 0.73
CBC_V5_WEIGHT = 0.27
CBC_V5_THRESHOLD = 0.465


def _safe_float(value: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if value is None:
            return default

        result = float(value)

        if result != result:
            return default

        return result

    except (TypeError, ValueError):
        return default


def _probability(result: Any) -> Optional[float]:
    """
    Extract pneumonia/CAP probability from a branch result.
    Supports common dictionary formats.
    """

    if result is None:
        return None

    if isinstance(result, (int, float)):
        value = _safe_float(result)

        if value is not None and 0.0 <= value <= 1.0:
            return value

        return None

    if not isinstance(result, dict):
        return None

    candidate_keys = [
        "pneumonia_probability",
        "cap_probability",
        "probability",
        "positive_probability",
        "pneumonia_prob",
        "cap_prob",
    ]

    for key in candidate_keys:
        value = _safe_float(result.get(key))

        if value is not None and 0.0 <= value <= 1.0:
            return value

    probabilities = result.get("probabilities")

    if isinstance(probabilities, dict):
        for key in [
            "Pneumonia",
            "pneumonia",
            "CAP",
            "cap",
            "positive",
            "Positive",
            "1",
        ]:
            value = _safe_float(probabilities.get(key))

            if value is not None and 0.0 <= value <= 1.0:
                return value

    return None


def _bacterial_probability(result: Any) -> Optional[float]:
    """
    CBC V5 uses ONLY prob_bacterial as the CBC signal.
    CBC is not independently converted into a CAP probability.
    """

    if result is None:
        return None

    if not isinstance(result, dict):
        return None

    for key in [
        "prob_bacterial",
        "bacterial_probability",
        "probability_bacterial",
    ]:
        value = _safe_float(result.get(key))

        if value is not None and 0.0 <= value <= 1.0:
            return value

    probabilities = result.get("probabilities")

    if isinstance(probabilities, dict):
        for key in [
            "bacterial",
            "Bacterial",
            "prob_bacterial",
        ]:
            value = _safe_float(probabilities.get(key))

            if value is not None and 0.0 <= value <= 1.0:
                return value

    return None


# ============================================================
# EVIDENCE-FUSE V4
# ============================================================

def evidence_fuse_v4(
    clinical_result: Any,
    vital_result: Any,
) -> Dict[str, Any]:
    """
    Locked Evidence-Fuse V4:

        V4 probability =
            0.73 * CLIN-NOTE V4
            +
            0.27 * VITAL-FUSE

    Decision threshold = 0.665
    """

    clinical_probability = _probability(clinical_result)
    vital_probability = _probability(vital_result)

    if clinical_probability is None:
        raise ValueError(
            "CLIN-NOTE V4 probability is required for Evidence-Fuse V4."
        )

    if vital_probability is None:
        raise ValueError(
            "VITAL-FUSE probability is required for Evidence-Fuse V4."
        )

    probability = (
        V4_NLP_WEIGHT * clinical_probability
        + V4_VITAL_WEIGHT * vital_probability
    )

    prediction = "Pneumonia" if probability >= V4_THRESHOLD else "Normal"

    return {
        "engine": "Evidence-Fuse V4",
        "probability": float(probability),
        "pneumonia_probability": float(probability),
        "prediction": prediction,
        "threshold": V4_THRESHOLD,
        "weights": {
            "clinical": V4_NLP_WEIGHT,
            "vital": V4_VITAL_WEIGHT,
        },
        "inputs": {
            "clinical_probability": clinical_probability,
            "vital_probability": vital_probability,
        },
    }


# ============================================================
# CBC V5
# ============================================================

def cbc_v5(
    evidence_fuse_v4_result: Any,
    cbc_result: Any,
) -> Dict[str, Any]:
    """
    Locked CBC V5:

        final probability =
            0.73 * Evidence-Fuse V4 probability
            +
            0.27 * prob_bacterial

    Threshold = 0.465

    CBC is optional.
    If CBC is missing, Evidence-Fuse V4 is returned unchanged.
    """

    v4_probability = _probability(evidence_fuse_v4_result)

    if v4_probability is None:
        raise ValueError(
            "Evidence-Fuse V4 probability is required for CBC V5."
        )

    bacterial_probability = _bacterial_probability(cbc_result)

    # --------------------------------------------------------
    # Missing CBC policy:
    # CBC is NOT required.
    # No artificial imputation.
    # Fallback = Evidence-Fuse V4.
    # --------------------------------------------------------

    if bacterial_probability is None:
        return {
            "engine": "CBC V5",
            "status": "CBC_MISSING_FALLBACK_V4",
            "probability": float(v4_probability),
            "pneumonia_probability": float(v4_probability),
            "prediction": (
                "Pneumonia"
                if v4_probability >= V4_THRESHOLD
                else "Normal"
            ),
            "threshold": V4_THRESHOLD,
            "used_cbc": False,
            "cbc_signal": None,
            "fallback": "Evidence-Fuse V4",
        }

    final_probability = (
        CBC_V5_V4_WEIGHT * v4_probability
        + CBC_V5_WEIGHT * bacterial_probability
    )

    prediction = (
        "Pneumonia"
        if final_probability >= CBC_V5_THRESHOLD
        else "Normal"
    )

    return {
        "engine": "CBC V5",
        "status": "FINAL",
        "probability": float(final_probability),
        "pneumonia_probability": float(final_probability),
        "prediction": prediction,
        "threshold": CBC_V5_THRESHOLD,
        "used_cbc": True,
        "cbc_signal": "prob_bacterial",
        "prob_bacterial": float(bacterial_probability),
        "weights": {
            "evidence_fuse_v4": CBC_V5_V4_WEIGHT,
            "cbc": CBC_V5_WEIGHT,
        },
        "inputs": {
            "evidence_fuse_v4_probability": float(v4_probability),
            "prob_bacterial": float(bacterial_probability),
        },
    }


# ============================================================
# SEVERITY ENGINE V1
# ============================================================

def severity_assessment(
    *,
    spo2: Any = None,
    cyanosis: bool = False,
    altered_consciousness: bool = False,
    hypoventilation: bool = False,
    respiratory_distress_count: int = 0,
    radiologic_complication: bool = False,
    tachypnea: bool = False,
    single_respiratory_distress: bool = False,
    unusual_sleepiness: bool = False,
    dehydration: bool = False,
    restlessness: bool = False,
) -> Dict[str, Any]:

    score = 0
    high_risk_flags = []
    moderate_signals = []

    spo2_value = _safe_float(spo2)

    # --------------------------------------------------------
    # HIGH-RISK FLAGS
    # --------------------------------------------------------

    if spo2_value is not None and spo2_value < 90:
        high_risk_flags.append("SpO2 < 90%")

    if cyanosis:
        high_risk_flags.append("cyanosis")

    if altered_consciousness:
        high_risk_flags.append("altered consciousness")

    if hypoventilation:
        high_risk_flags.append("hypoventilation")

    if respiratory_distress_count >= 2:
        high_risk_flags.append("multiple respiratory distress signs")

    if radiologic_complication:
        high_risk_flags.append("possible radiologic complication")

    # --------------------------------------------------------
    # MODERATE SIGNALS
    # --------------------------------------------------------

    if spo2_value is not None and 90 <= spo2_value <= 93:
        score += 2
        moderate_signals.append("SpO2 90–93%")

    if tachypnea:
        score += 2
        moderate_signals.append("age-adjusted tachypnea signal")

    if single_respiratory_distress:
        score += 2
        moderate_signals.append("single respiratory distress sign")

    if unusual_sleepiness:
        score += 1
        moderate_signals.append("unusual sleepiness")

    if dehydration:
        score += 1
        moderate_signals.append("dehydration signs")

    if restlessness:
        score += 1
        moderate_signals.append("restlessness")

    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

    if high_risk_flags or score >= 6:
        severity = "HIGH"

    elif 2 <= score <= 5:
        severity = "MODERATE"

    else:
        severity = "LOW"

    return {
        "engine": "CAPGuard Severity Assessment Engine V1",
        "severity": severity,
        "score": score,
        "high_risk_flags": high_risk_flags,
        "moderate_signals": moderate_signals,
        "clinical_status": "decision_support_only",
    }


# ============================================================
# TREATMENT DECISION SUPPORT
# ============================================================

def treatment_guidance(
    *,
    severity: str,
    bacterial_probability: Any = None,
    radiologic_complication: Optional[str] = None,
) -> Dict[str, Any]:

    recommendations = [
        "Assess severity and respiratory stability first.",
        "Check oxygenation and work of breathing.",
        "Support hydration and nutrition as clinically appropriate.",
        "Review likelihood of bacterial versus non-bacterial disease.",
        "Consider antimicrobial stewardship and local resistance patterns.",
        "Arrange clinician-directed follow-up.",
    ]

    alerts = []

    if severity == "HIGH":
        alerts.append(
            "Escalation assessment is recommended because high-risk "
            "severity signals are present."
        )

        recommendations.append(
            "Escalate when hypoxemia, respiratory distress, altered "
            "consciousness, or deterioration occurs."
        )

    if radiologic_complication:
        complication = radiologic_complication.lower()

        if "moderate" in complication or "large" in complication:
            recommendations.append(
                "Consider chest ultrasound to characterize effusion "
                "size and complexity."
            )

        if "small" in complication and "uncomplicated" in complication:
            recommendations.append(
                "Observation may be appropriate depending on clinical context."
            )

        if (
            "moderate" in complication
            and "respiratory distress" in complication
        ):
            recommendations.append(
                "Specialist/hospital assessment and drainage evaluation."
            )

        if "large" in complication or "purulent" in complication:
            recommendations.append(
                "Hospital/specialist drainage evaluation."
            )

        if "empyema" in complication:
            recommendations.append(
                "Specialist management; drainage strategy is "
                "clinician-directed."
            )

        alerts.append(
            "Possible pleural complication detected; clinician evaluation required."
        )

    bacterial = _safe_float(bacterial_probability)

    return {
        "engine": "CAPGuard Treatment Decision Support",
        "recommendations": recommendations,
        "alerts": alerts,
        "bacterial_signal": bacterial,
        "not_a_prescription": True,
        "no_dosing": True,
        "no_autonomous_antibiotic_selection": True,
        "human_confirmation_required": True,
    }


# ============================================================
# COMPLETE PRODUCTION PIPELINE
# ============================================================

def run_production_pipeline(
    *,
    clinical_result: Any,
    vital_result: Any,
    cbc_result: Any = None,
    severity_inputs: Optional[Dict[str, Any]] = None,
    radiologic_complication: Optional[str] = None,
) -> Dict[str, Any]:

    # Stage 1: Evidence-Fuse V4
    v4_result = evidence_fuse_v4(
        clinical_result=clinical_result,
        vital_result=vital_result,
    )

    # Stage 2: CBC V5
    final_result = cbc_v5(
        evidence_fuse_v4_result=v4_result,
        cbc_result=cbc_result,
    )

    # Stage 3: Severity
    severity_inputs = severity_inputs or {}

    severity_result = severity_assessment(
        spo2=severity_inputs.get("spo2"),
        cyanosis=bool(severity_inputs.get("cyanosis", False)),
        altered_consciousness=bool(
            severity_inputs.get("altered_consciousness", False)
        ),
        hypoventilation=bool(
            severity_inputs.get("hypoventilation", False)
        ),
        respiratory_distress_count=int(
            severity_inputs.get("respiratory_distress_count", 0)
        ),
        radiologic_complication=bool(
            severity_inputs.get("radiologic_complication", False)
        ),
        tachypnea=bool(severity_inputs.get("tachypnea", False)),
        single_respiratory_distress=bool(
            severity_inputs.get("single_respiratory_distress", False)
        ),
        unusual_sleepiness=bool(
            severity_inputs.get("unusual_sleepiness", False)
        ),
        dehydration=bool(
            severity_inputs.get("dehydration", False)
        ),
        restlessness=bool(
            severity_inputs.get("restlessness", False)
        ),
    )

    # Stage 4: Treatment / CDS
    treatment_result = treatment_guidance(
        severity=severity_result["severity"],
        bacterial_probability=_bacterial_probability(cbc_result),
        radiologic_complication=radiologic_complication,
    )

    return {
        "engine": ENGINE_VERSION,
        "status": "SUCCESS",
        "final_prediction": final_result,
        "evidence_fuse_v4": v4_result,
        "severity": severity_result,
        "treatment": treatment_result,
    }


# ============================================================
# STATUS
# ============================================================

def system_status() -> Dict[str, Any]:
    return {
        "engine": ENGINE_VERSION,
        "status": "READY",
        "evidence_fuse_v4": {
            "nlp_weight": V4_NLP_WEIGHT,
            "vital_weight": V4_VITAL_WEIGHT,
            "threshold": V4_THRESHOLD,
        },
        "cbc_v5": {
            "v4_weight": CBC_V5_V4_WEIGHT,
            "cbc_weight": CBC_V5_WEIGHT,
            "signal": "prob_bacterial",
            "threshold": CBC_V5_THRESHOLD,
            "cbc_required": False,
            "fallback": "Evidence-Fuse V4",
        },
        "safety": {
            "retraining": False,
            "test_weight_search": False,
            "test_threshold_search": False,
            "validation_configuration_locked": True,
        },
    }


if __name__ == "__main__":
    import json

    print(
        json.dumps(
            system_status(),
            indent=2,
            ensure_ascii=False,
        )
    )