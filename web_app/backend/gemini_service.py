import os
import json
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.7-flash")

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured in the backend .env file."
    )

client = genai.Client(api_key=GEMINI_API_KEY)


# ============================================================
# CAPGUARD → GEMINI PAYLOAD
# ============================================================

def build_gemini_payload(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract only the clinically relevant CAPGuard output.

    Gemini does NOT perform the diagnosis.
    CAPGuard remains the source of:
        - final prediction
        - probabilities
        - fusion result
        - severity
        - treatment guidance
        - branch outputs
    """

    return {
        "patient": result.get("patient"),

        "final_result": result.get("result"),

        "fusion": result.get("fusion"),

        "decision_explanation": result.get(
            "decision_explanation"
        ),

        "xray_branch": (
            result.get("branches", {})
            .get("xray")
        ),

        "clinical_nlp_branch": (
            result.get("branches", {})
            .get("clinical_nlp")
        ),

        "vital_branch": (
            result.get("branches", {})
            .get("vital")
        ),

        "severity": result.get("severity"),

        "treatment": result.get("treatment"),

        "modalities": result.get("modalities"),

        "production_models": result.get(
            "production_models"
        ),
    }


# ============================================================
# GEMINI SYSTEM INSTRUCTIONS
# ============================================================

SYSTEM_INSTRUCTION = """
You are the generative clinical reasoning and explanation layer
for CAPGuard AI.

IMPORTANT ARCHITECTURE RULE:

CAPGuard AI is the actual medical AI system.

The CAPGuard trained models and production engine are authoritative
for the medical prediction.

You are NOT the diagnostic engine.

You MUST NOT:
- change the CAPGuard final prediction
- change pneumonia probability
- recalculate Evidence-Fuse V4
- override CAPGuard probabilities
- invent clinical findings
- invent laboratory values
- invent X-ray findings
- invent patient information
- prescribe medications
- provide antibiotic doses
- replace the CAPGuard severity engine
- replace the CAPGuard treatment guidance engine

You SHOULD:
- explain the CAPGuard result clearly
- summarize the available evidence
- explain how the different branches contributed
- explain important agreement or disagreement between modalities
- highlight uncertainty or conflicts
- explain risk in clinically understandable language
- provide appropriate recommendations for clinical review
- preserve the exact CAPGuard prediction and probabilities

The treatment information supplied by CAPGuard is decision-support
guidance and must not be presented as an autonomous prescription.

A qualified clinician must make the final clinical decision.

Return ONLY valid JSON.

Required JSON structure:

{
  "summary": "...",
  "key_findings": [
    "...",
    "..."
  ],
  "evidence_interpretation": "...",
  "risk_interpretation": "...",
  "imaging_interpretation": "...",
  "clinical_cautions": [
    "...",
    "..."
  ],
  "recommended_review": "...",
  "disclaimer": "Clinical decision support only. Final assessment must be confirmed by a qualified clinician."
}
"""


# ============================================================
# JSON PARSER
# ============================================================

def parse_json_response(text: str) -> Dict[str, Any]:
    """
    Safely parse Gemini JSON output.
    Handles plain JSON and accidental markdown fences.
    """

    if not text:
        raise ValueError("Gemini returned an empty response.")

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = cleaned.replace("```json", "", 1)
        cleaned = cleaned.replace("```", "")
        cleaned = cleaned.strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Gemini returned invalid JSON: {exc}"
        ) from exc

    if not isinstance(parsed, dict):
        raise ValueError(
            "Gemini response must be a JSON object."
        )

    return parsed


# ============================================================
# MAIN GEMINI FUNCTION
# ============================================================

def generate_clinical_reasoning(
    capguard_result: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate an explanatory clinical reasoning layer from
    CAPGuard's existing structured output.

    Gemini does NOT replace CAPGuard.
    """

    payload = build_gemini_payload(capguard_result)

    prompt = f"""
Analyze the following CAPGuard AI assessment.

Use ONLY the information contained in this CAPGuard output.

Do not modify or reinterpret the final CAPGuard prediction.

CAPGuard assessment:

{json.dumps(payload, ensure_ascii=False, indent=2, default=str)}
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "temperature": 0.2,
                "response_mime_type": "application/json",
            },
        )

        reasoning = parse_json_response(
            response.text
        )

        return {
            "status": "success",
            "provider": "Google Gemini",
            "model": GEMINI_MODEL,
            "reasoning": reasoning,
        }

    except Exception as exc:
        return {
            "status": "UNAVAILABLE",
            "provider": "Google Gemini",
            "model": GEMINI_MODEL,
            "error": str(exc),
            "reasoning": None,
        }