"""
PneumoCare AI
Treatment Engine V1

Consumes structured clinical findings and returns
a conservative treatment-plan object.

No medication doses are produced.
"""

from typing import Any, Dict, Optional

from treatment_rules_v1 import (
    RULE_VERSION,
    WHO_SOURCE,
    TREATMENT_RULES,
)


def _to_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _age_months(age: Any, age_unit: str = "years") -> Optional[float]:
    value = _to_float(age)

    if value is None:
        return None

    if age_unit.lower() in {"month", "months", "mo"}:
        return value

    return value * 12.0


def generate_treatment_plan(
    age: Any,
    age_unit: str = "years",
    pneumonia_assessment: bool = False,
    fast_breathing: bool = False,
    chest_indrawing: bool = False,
    general_danger_sign: bool = False,
    spo2: Any = None,
) -> Dict[str, Any]:

    months = _age_months(age, age_unit)

    result = {
        "engine": "PneumoCare Treatment Engine",
        "version": RULE_VERSION,
        "status": "CLINICIAN_REVIEW",
        "disposition": "CLINICIAN_REVIEW",
        "antimicrobial_options": [],
        "supportive_care": [],
        "monitoring": [],
        "red_flags": [],
        "rationale": [],
        "evidence_source": WHO_SOURCE,
        "requires_clinician": True,
        "dose_provided": False,
    }

    # ---------------------------------------------------------
    # Rule 1: General danger signs
    # ---------------------------------------------------------
    if general_danger_sign:
        rule = TREATMENT_RULES["DANGER_SIGNS"]

        result.update({
            "status": "URGENT",
            "disposition": rule["disposition"],
            "monitoring": rule["monitoring"],
            "rationale": [
                "General danger sign detected."
            ],
            "red_flags": [
                "General danger sign"
            ],
        })

        return result

    # ---------------------------------------------------------
    # Rule 2: Hypoxaemia
    # ---------------------------------------------------------
    spo2_value = _to_float(spo2)

    if spo2_value is not None and spo2_value < 90:
        rule = TREATMENT_RULES["HYPOXAEMIA"]

        result.update({
            "status": "URGENT",
            "disposition": rule["disposition"],
            "supportive_care": rule["supportive_care"],
            "monitoring": rule["monitoring"],
            "rationale": [
                "SpO2 is below the configured hypoxaemia threshold."
            ],
            "red_flags": [
                "Hypoxaemia"
            ],
        })

        return result

    # ---------------------------------------------------------
    # No pneumonia assessment
    # ---------------------------------------------------------
    if not pneumonia_assessment:
        result["rationale"].append(
            "No pneumonia assessment is available."
        )
        return result

    # ---------------------------------------------------------
    # Rule 3: Age 2-59 months
    # ---------------------------------------------------------
    if months is not None and 2 <= months <= 59:

        if chest_indrawing:
            rule = TREATMENT_RULES[
                "2_59_MONTHS_CHEST_INDRAWING"
            ]

            result.update({
                "status": "RECOMMENDED",
                "disposition": rule["disposition"],
                "antimicrobial_options": rule[
                    "antimicrobial_options"
                ],
                "supportive_care": rule[
                    "supportive_care"
                ],
                "monitoring": rule["monitoring"],
                "rationale": [
                    "Pneumonia with chest indrawing "
                    "and no detected general danger sign."
                ],
            })

            return result

        if fast_breathing:
            rule = TREATMENT_RULES[
                "2_59_MONTHS_FAST_BREATHING"
            ]

            result.update({
                "status": "RECOMMENDED",
                "disposition": rule["disposition"],
                "antimicrobial_options": rule[
                    "antimicrobial_options"
                ],
                "supportive_care": rule[
                    "supportive_care"
                ],
                "monitoring": rule["monitoring"],
                "rationale": [
                    "Pneumonia with fast breathing "
                    "and no detected general danger sign."
                ],
            })

            return result

    # ---------------------------------------------------------
    # Rule 4: Age 5-9 years
    # ---------------------------------------------------------
    if months is not None and 60 <= months <= 119:
        rule = TREATMENT_RULES["AGE_5_9_YEARS"]

        result.update({
            "status": "CLINICIAN_REVIEW",
            "disposition": rule["disposition"],
            "monitoring": rule["monitoring"],
            "rationale": [
                rule["reason"]
            ],
        })

        return result

    # ---------------------------------------------------------
    # Unsupported / incomplete case
    # ---------------------------------------------------------
    result["rationale"].append(
        "Available clinical information does not match "
        "a configured treatment rule."
    )

    return result


if __name__ == "__main__":

    print("=" * 70)
    print("PneumoCare AI — Treatment Engine V1 TEST")
    print("=" * 70)

    tests = [
        {
            "name": "2-59 months + fast breathing",
            "args": {
                "age": 3,
                "age_unit": "years",
                "pneumonia_assessment": True,
                "fast_breathing": True,
            },
        },
        {
            "name": "2-59 months + chest indrawing",
            "args": {
                "age": 2,
                "age_unit": "years",
                "pneumonia_assessment": True,
                "chest_indrawing": True,
            },
        },
        {
            "name": "General danger sign",
            "args": {
                "age": 3,
                "age_unit": "years",
                "pneumonia_assessment": True,
                "general_danger_sign": True,
            },
        },
        {
            "name": "Hypoxaemia",
            "args": {
                "age": 3,
                "age_unit": "years",
                "pneumonia_assessment": True,
                "fast_breathing": True,
                "spo2": 88,
            },
        },
        {
            "name": "5-9 years",
            "args": {
                "age": 7,
                "age_unit": "years",
                "pneumonia_assessment": True,
                "fast_breathing": True,
            },
        },
    ]

    for test in tests:
        print("\n" + "-" * 70)
        print(test["name"])
        print("-" * 70)

        plan = generate_treatment_plan(**test["args"])

        print("STATUS:", plan["status"])
        print("DISPOSITION:", plan["disposition"])
        print(
            "ANTIMICROBIAL OPTIONS:",
            plan["antimicrobial_options"]
        )
        print(
            "DOSE PROVIDED:",
            plan["dose_provided"]
        )
        print(
            "REQUIRES CLINICIAN:",
            plan["requires_clinician"]
        )
        print(
            "RATIONALE:",
            plan["rationale"]
        )