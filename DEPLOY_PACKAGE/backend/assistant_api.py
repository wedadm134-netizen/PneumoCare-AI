import os
import json
import time
from typing import Optional, Dict, Any, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from dotenv import load_dotenv
from google import genai
from google.genai import types

from treatment_engine import generate_treatment_plan


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

configured_model = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite",
).strip()

# Retired model protection
if configured_model == "gemini-2.5-flash-lite":
    configured_model = "gemini-3.5-flash-lite"

GEMINI_MODEL = configured_model

GEMINI_FALLBACK_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
]

GEMINI_RETRIES_ON_TIMEOUT = 1
GEMINI_RETRY_DELAY_SECONDS = 1
GEMINI_TIMEOUT_MS = 45000
GEMINI_MAX_OUTPUT_TOKENS = 800


# ============================================================
# GEMINI CLIENT
# ============================================================

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not configured in the backend .env file."
    )


gemini_client = genai.Client(
    api_key=GEMINI_API_KEY,
    http_options=types.HttpOptions(
        timeout=GEMINI_TIMEOUT_MS,
    ),
)


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/assistant",
    tags=["Clinical AI Assistant"],
)


# ============================================================
# REQUEST / RESPONSE SCHEMAS
# ============================================================

class AssistantChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
    )

    language: str = Field(
        default="en",
        pattern="^(en|ar)$",
    )

    patient: Optional[Dict[str, Any]] = None

    assessment: Optional[Dict[str, Any]] = None

    visit: Optional[Dict[str, Any]] = None


class AssistantChatResponse(BaseModel):
    assistant: str

    answer: str

    language: str

    safety_flag: bool

    safety_message: str

    context_used: Dict[str, Any]

    status: str

    treatment_plan: Optional[Dict[str, Any]] = None


# ============================================================
# GENERAL HELPERS
# ============================================================

def first_value(
    data: Optional[Dict[str, Any]],
    *keys: str,
    default: Any = None,
) -> Any:

    if not data:
        return default

    for key in keys:
        value = data.get(key)

        if value is not None:
            return value

    return default


def parse_bool(value: Any) -> bool:

    if isinstance(value, bool):
        return value

    if value is None:
        return False

    if isinstance(value, (int, float)):
        return bool(value)

    if isinstance(value, str):

        normalized = value.strip().lower()

        if normalized in {
            "true",
            "1",
            "yes",
            "y",
            "positive",
            "present",
        }:
            return True

        if normalized in {
            "false",
            "0",
            "no",
            "n",
            "negative",
            "absent",
        }:
            return False

    return False


def safe_probability(
    value: Any,
    default: float = 0.0,
) -> float:

    try:
        probability = float(value)

    except (TypeError, ValueError):
        return default

    if probability > 1:
        probability = probability / 100.0

    probability = max(
        0.0,
        min(
            1.0,
            probability,
        ),
    )

    return probability


def prediction_is_pneumonia(
    prediction: Any,
) -> bool:

    if prediction is None:
        return False

    text = str(prediction).strip().lower()

    return (
        "pneumonia" in text
        or "positive" in text
        or text == "1"
        or text == "true"
    )


# ============================================================
# SAFETY SIGNAL DETECTION
# ============================================================

def detect_safety_signals(
    patient: Optional[Dict[str, Any]],
    assessment: Optional[Dict[str, Any]],
    visit: Optional[Dict[str, Any]],
) -> Dict[str, Any]:

    patient = patient or {}
    assessment = assessment or {}
    visit = visit or {}

    spo2 = first_value(
        assessment,
        "spo2",
        "spo2_pct",
        "oxygen_saturation",
        default=first_value(
            visit,
            "spo2",
            "spo2_pct",
            "oxygen_saturation",
        ),
    )

    respiratory_rate = first_value(
        assessment,
        "respiratory_rate",
        "resp_rate",
        "rr",
        default=first_value(
            visit,
            "respiratory_rate",
            "resp_rate",
            "rr",
        ),
    )

    chest_indrawing = parse_bool(
        first_value(
            assessment,
            "chest_indrawing",
            "chest_indrawing_present",
            default=first_value(
                visit,
                "chest_indrawing",
                "chest_indrawing_present",
            ),
        )
    )

    general_danger_sign = parse_bool(
        first_value(
            assessment,
            "general_danger_sign",
            "danger_sign",
            "danger_signs",
            default=first_value(
                visit,
                "general_danger_sign",
                "danger_sign",
                "danger_signs",
            ),
        )
    )

    cyanosis = parse_bool(
        first_value(
            assessment,
            "cyanosis",
            default=first_value(
                visit,
                "cyanosis",
            ),
        )
    )

    disorders_of_consciousness = parse_bool(
        first_value(
            assessment,
            "disorders_of_consciousness",
            "altered_consciousness",
            default=first_value(
                visit,
                "disorders_of_consciousness",
                "altered_consciousness",
            ),
        )
    )

    dehydration_signs = parse_bool(
        first_value(
            assessment,
            "dehydration_signs",
            "dehydration",
            default=first_value(
                visit,
                "dehydration_signs",
                "dehydration",
            ),
        )
    )

    nasal_flaring = parse_bool(
        first_value(
            assessment,
            "nasal_flaring",
            default=first_value(
                visit,
                "nasal_flaring",
            ),
        )
    )

    urgent_reasons = []

    try:
        if spo2 is not None:

            spo2_value = float(spo2)

            if spo2_value < 90:
                urgent_reasons.append(
                    "SpO2 below 90%"
                )

    except (TypeError, ValueError):
        pass

    if chest_indrawing:
        urgent_reasons.append(
            "Chest indrawing"
        )

    if general_danger_sign:
        urgent_reasons.append(
            "General danger sign"
        )

    if cyanosis:
        urgent_reasons.append(
            "Cyanosis"
        )

    if disorders_of_consciousness:
        urgent_reasons.append(
            "Altered consciousness"
        )

    if dehydration_signs:
        urgent_reasons.append(
            "Dehydration signs"
        )

    safety_flag = len(urgent_reasons) > 0

    if safety_flag:
        safety_message = (
            "Urgent clinical assessment may be required "
            "because one or more concerning clinical signals "
            "are present."
        )

    else:
        safety_message = (
            "No automatic emergency signal was identified "
            "from the supplied data."
        )

    return {
        "safety_flag": safety_flag,
        "safety_message": safety_message,
        "urgent_reasons": urgent_reasons,
        "spo2": spo2,
        "respiratory_rate": respiratory_rate,
        "chest_indrawing": chest_indrawing,
        "general_danger_sign": general_danger_sign,
        "cyanosis": cyanosis,
        "disorders_of_consciousness": disorders_of_consciousness,
        "dehydration_signs": dehydration_signs,
        "nasal_flaring": nasal_flaring,
    }


# ============================================================
# BRANCH EVIDENCE
# ============================================================

def extract_branch_evidence(
    assessment: Optional[Dict[str, Any]],
) -> Dict[str, Any]:

    assessment = assessment or {}

    # --------------------------------------------------------
    # Clinical + Laboratory / Fusion branch
    # --------------------------------------------------------

    final_pneumonia_probability = first_value(
        assessment,
        "pneumonia_probability",
        "final_pneumonia_probability",
        "fusion_pneumonia_probability",
        "clinical_pneumonia_probability",
    )

    final_normal_probability = first_value(
        assessment,
        "normal_probability",
        "final_normal_probability",
        "fusion_normal_probability",
        "clinical_normal_probability",
    )

    final_prediction = first_value(
        assessment,
        "prediction",
        "final_prediction",
        "diagnosis",
        "final_assessment",
    )

    # --------------------------------------------------------
    # X-Ray branch
    # --------------------------------------------------------

    xray_probability = first_value(
        assessment,
        "xray_pneumonia_probability",
        "xray_probability",
        "image_pneumonia_probability",
    )

    xray_normal_probability = first_value(
        assessment,
        "xray_normal_probability",
        "image_normal_probability",
    )

    xray_prediction = first_value(
        assessment,
        "xray_prediction",
        "image_prediction",
        "xray_result",
    )

    return {
        "final_clinical_assessment": {
            "prediction": final_prediction,
            "pneumonia_probability": (
                safe_probability(final_pneumonia_probability)
                if final_pneumonia_probability is not None
                else None
            ),
            "normal_probability": (
                safe_probability(final_normal_probability)
                if final_normal_probability is not None
                else None
            ),
        },

        "xray_assessment": {
            "prediction": xray_prediction,
            "pneumonia_probability": (
                safe_probability(xray_probability)
                if xray_probability is not None
                else None
            ),
            "normal_probability": (
                safe_probability(xray_normal_probability)
                if xray_normal_probability is not None
                else None
            ),
        },
    }


# ============================================================
# CLINICAL CONTEXT
# ============================================================

def build_clinical_context(
    patient: Optional[Dict[str, Any]],
    assessment: Optional[Dict[str, Any]],
    visit: Optional[Dict[str, Any]],
    safety_signals: Dict[str, Any],
) -> Dict[str, Any]:

    patient = patient or {}
    assessment = assessment or {}
    visit = visit or {}

    age = first_value(
        patient,
        "age",
        "age_months",
        default=first_value(
            assessment,
            "age",
            "age_months",
        ),
    )

    age_unit = first_value(
        patient,
        "age_unit",
        default=first_value(
            assessment,
            "age_unit",
            default="months",
        ),
    )

    sex = first_value(
        patient,
        "sex",
        "gender",
    )

    pneumonia_prediction = first_value(
        assessment,
        "prediction",
        "final_prediction",
        "diagnosis",
        "final_assessment",
    )

    pneumonia_assessment = prediction_is_pneumonia(
        pneumonia_prediction
    )

    fast_breathing = parse_bool(
        first_value(
            assessment,
            "fast_breathing",
            "fast_breathing_present",
            default=first_value(
                visit,
                "fast_breathing",
                "fast_breathing_present",
            ),
        )
    )

    chest_indrawing = safety_signals[
        "chest_indrawing"
    ]

    general_danger_sign = safety_signals[
        "general_danger_sign"
    ]

    spo2 = safety_signals[
        "spo2"
    ]

    return {
        "patient": {
            "age": age,
            "age_unit": age_unit,
            "sex": sex,
        },

        "assessment": {
            "pneumonia_prediction": pneumonia_prediction,
            "pneumonia_assessment": pneumonia_assessment,
        },

        "clinical_signals": {
            "fast_breathing": fast_breathing,
            "chest_indrawing": chest_indrawing,
            "general_danger_sign": general_danger_sign,
            "spo2": spo2,
        },

        "branch_evidence": extract_branch_evidence(
            assessment
        ),

        "safety": safety_signals,
    }


# ============================================================
# GEMINI MODEL DISCOVERY
# ============================================================

def get_available_gemini_models() -> List[str]:

    discovered = []

    try:

        for model in gemini_client.models.list():

            name = getattr(
                model,
                "name",
                None,
            )

            if not name:
                continue

            name = str(name)

            if name.startswith("models/"):
                name = name[len("models/"):]

            if not name.startswith("gemini-"):
                continue

            supported_actions = getattr(
                model,
                "supported_actions",
                None,
            )

            if supported_actions:

                normalized_actions = {
                    str(action).lower()
                    for action in supported_actions
                }

                if "generatecontent" not in normalized_actions:
                    continue

            if name not in discovered:
                discovered.append(name)

    except Exception as exc:

        print(
            "[Gemini] Model discovery failed:",
            str(exc),
        )

    return discovered


# ============================================================
# BUILD MODEL CANDIDATES
# ============================================================

def build_model_candidates() -> List[str]:

    candidates = []

    def add_model(
        model_name: Optional[str],
    ):

        if not model_name:
            return

        model_name = model_name.strip()

        if not model_name:
            return

        # ----------------------------------------------------
        # FIXED:
        # Correctly remove "models/" prefix.
        # ----------------------------------------------------

        if model_name.startswith("models/"):
            model_name = model_name[len("models/"):]

        # Explicitly reject retired model.

        if model_name == "gemini-2.5-flash-lite":
            return

        if model_name not in candidates:
            candidates.append(model_name)

    # Configured model first.

    add_model(
        GEMINI_MODEL
    )

    # Known fallback models.

    for model_name in GEMINI_FALLBACK_MODELS:
        add_model(model_name)

    # Dynamically discovered models.

    discovered = get_available_gemini_models()

    # Prefer Flash models.

    discovered.sort(
        key=lambda name: (
            0 if "flash" in name.lower() else 1,
            0 if "lite" in name.lower() else 1,
            name,
        )
    )

    for model_name in discovered:
        add_model(model_name)

    return candidates


# ============================================================
# GEMINI ERROR CLASSIFICATION
# ============================================================

def classify_gemini_error(
    exc: Exception,
) -> str:

    error_text = str(exc).lower()

    status_code = getattr(
        exc,
        "code",
        None,
    )

    if status_code is not None:

        status_code = str(
            status_code
        )

    # 404 / model unavailable

    if (
        "404" in error_text
        or "not_found" in error_text
        or "model not found" in error_text
    ):
        return "MODEL_NOT_FOUND"

    # 503 / temporary capacity issue

    if (
        "503" in error_text
        or "unavailable" in error_text
        or "high demand" in error_text
        or "service unavailable" in error_text
    ):
        return "UNAVAILABLE"

    # 429 / quota or rate limit

    if (
        "429" in error_text
        or "resource_exhausted" in error_text
        or "rate limit" in error_text
        or "quota" in error_text
    ):
        return "RATE_LIMITED"

    # 504 / timeout

    if (
        "504" in error_text
        or "deadline_exceeded" in error_text
        or "deadline expired" in error_text
        or "timeout" in error_text
        or "timed out" in error_text
    ):
        return "TIMEOUT"

    # 500

    if (
        "500" in error_text
        or "internal server error" in error_text
    ):
        return "SERVER_ERROR"

    # 502

    if (
        "502" in error_text
        or "bad gateway" in error_text
    ):
        return "GATEWAY_ERROR"

    return "UNKNOWN"


# ============================================================
# GEMINI REQUEST
# ============================================================

def ask_gemini(
    question: str,
    language: str,
    clinical_context: Dict[str, Any],
    safety_signals: Dict[str, Any],
    treatment_plan: Optional[Dict[str, Any]],
) -> str:

    # --------------------------------------------------------
    # System instruction
    # --------------------------------------------------------

    if language == "ar":

        language_instruction = """
Respond in Arabic.
Use clear professional medical Arabic.
Keep important clinical terms understandable.
Do not expose internal model names, weights,
thresholds, implementation details, or code.
"""

    else:

        language_instruction = """
Respond in clear professional English.
Do not expose internal model names, weights,
thresholds, implementation details, or code.
"""

    system_instruction = f"""
You are the conversational clinical AI assistant
inside PneumoCare AI.

PneumoCare AI is a clinical decision-support system.

IMPORTANT AUTHORITY RULE:

The structured clinical assessment generated by
PneumoCare AI is authoritative for the patient's
computed AI assessment.

You must NOT change, override, invent, or recalculate
the official assessment probabilities.

Your role is to explain the supplied evidence clearly
and safely.

You are NOT the final diagnostic authority.

You must encourage appropriate clinician review when
clinical judgment is required.

------------------------------------------------------------
EVIDENCE RULES
------------------------------------------------------------

The supplied context may contain:

1. Final Clinical Assessment
   - Based on the clinical and laboratory evidence.

2. X-Ray Assessment
   - Based on the chest X-ray evidence.

3. Safety / Vital Signals
   - Including SpO2 and danger signs.

When these sources disagree:

- Do NOT hide the disagreement.
- Explain the disagreement clearly.
- Do NOT manufacture a consensus.
- Do NOT change the supplied probabilities.

------------------------------------------------------------
SAFETY RULES
------------------------------------------------------------

If urgent clinical signals are present, clearly advise
urgent clinical assessment.

If SpO2 is below 90%, treat this as a concerning
clinical signal requiring prompt clinical attention.

Do not provide false reassurance.

Do not claim that the patient is definitely normal
based only on a model result.

------------------------------------------------------------
TREATMENT RULES
------------------------------------------------------------

The treatment plan supplied in the context comes from
the PneumoCare Treatment Engine.

The Treatment Engine is authoritative for the
structured treatment recommendation.

Do NOT invent a different antimicrobial regimen.

Do NOT replace the Treatment Engine recommendation.

If the treatment plan indicates that clinician review
is required, say so clearly.

Do not present treatment as a substitute for clinical
assessment.

------------------------------------------------------------
RESPONSE STYLE
------------------------------------------------------------

Be concise, clinically useful, and easy to understand.

Focus on:

- What the supplied evidence means.
- Whether the evidence is reassuring or concerning.
- Any conflict between clinical/lab and X-ray evidence.
- Safety concerns.
- What should be discussed with the clinician.

{language_instruction}

------------------------------------------------------------
SUPPLIED CAPGUARD / PNEUMOCARE DATA
------------------------------------------------------------

Clinical Context:

{json.dumps(
    clinical_context,
    ensure_ascii=False,
    indent=2,
)}

Safety Signals:

{json.dumps(
    safety_signals,
    ensure_ascii=False,
    indent=2,
)}

Treatment Engine Result:

{json.dumps(
    treatment_plan,
    ensure_ascii=False,
    indent=2,
)}

------------------------------------------------------------
USER QUESTION
------------------------------------------------------------

{question}
"""

    models_to_try = build_model_candidates()

    if not models_to_try:

        raise RuntimeError(
            "No Gemini models are available."
        )

    print(
        "[Gemini] Models to try:",
        models_to_try,
    )

    last_error = None
    last_model = None

    # ========================================================
    # MODEL LOOP
    # ========================================================

    for model_name in models_to_try:

        last_model = model_name

        timeout_attempts = 0

        while True:

            try:

                print(
                    f"[Gemini] Trying model: {model_name}"
                )

                response = (
                    gemini_client.models.generate_content(
                        model=model_name,
                        contents=system_instruction,
                        config=types.GenerateContentConfig(
                            temperature=0.1,
                            max_output_tokens=GEMINI_MAX_OUTPUT_TOKENS,
                        ),
                    )
                )

                answer = getattr(
                    response,
                    "text",
                    None,
                )

                if answer:

                    answer = answer.strip()

                    if answer:
                        print(
                            f"[Gemini] Success: {model_name}"
                        )

                        return answer

                raise RuntimeError(
                    "Gemini returned an empty response."
                )

            except Exception as exc:

                last_error = exc

                error_type = classify_gemini_error(
                    exc
                )

                print(
                    "[Gemini] Error:",
                    {
                        "model": model_name,
                        "type": error_type,
                        "error": str(exc),
                    },
                )

                # ------------------------------------------------
                # Model does not exist / unavailable
                # ------------------------------------------------

                if error_type == "MODEL_NOT_FOUND":

                    print(
                        f"[Gemini] Skipping unavailable model: "
                        f"{model_name}"
                    )

                    break

                # ------------------------------------------------
                # 503 high demand
                # ------------------------------------------------

                if error_type == "UNAVAILABLE":

                    print(
                        f"[Gemini] Model unavailable, "
                        f"moving to next model: {model_name}"
                    )

                    break

                # ------------------------------------------------
                # 429 rate limit
                # ------------------------------------------------

                if error_type == "RATE_LIMITED":

                    print(
                        f"[Gemini] Rate limited, "
                        f"moving to next model: {model_name}"
                    )

                    time.sleep(
                        GEMINI_RETRY_DELAY_SECONDS
                    )

                    break

                # ------------------------------------------------
                # Timeout / 504
                # ------------------------------------------------

                if error_type == "TIMEOUT":

                    if (
                        timeout_attempts
                        < GEMINI_RETRIES_ON_TIMEOUT
                    ):

                        timeout_attempts += 1

                        print(
                            "[Gemini] Timeout detected. "
                            "Retrying same model..."
                        )

                        time.sleep(
                            GEMINI_RETRY_DELAY_SECONDS
                        )

                        continue

                    print(
                        "[Gemini] Timeout retry exhausted. "
                        "Moving to next model."
                    )

                    break

                # ------------------------------------------------
                # 500 / 502
                # ------------------------------------------------

                if error_type in {
                    "SERVER_ERROR",
                    "GATEWAY_ERROR",
                }:

                    print(
                        "[Gemini] Temporary server error. "
                        "Moving to next model."
                    )

                    break

                # ------------------------------------------------
                # Unknown error
                # ------------------------------------------------

                raise RuntimeError(
                    f"Gemini request failed for model "
                    f"{model_name}: {exc}"
                ) from exc

    # ========================================================
    # ALL MODELS FAILED
    # ========================================================

    if last_error is not None:

        error_type = classify_gemini_error(
            last_error
        )

        raise RuntimeError(
            "Gemini is currently unavailable. "
            f"Last model: {last_model}. "
            f"Error type: {error_type}. "
            f"Details: {last_error}"
        )

    raise RuntimeError(
        "Gemini could not generate a response."
    )


# ============================================================
# CHAT ENDPOINT
# ============================================================

@router.post(
    "/chat",
    response_model=AssistantChatResponse,
)
def assistant_chat(
    request: AssistantChatRequest,
):

    try:

        # ====================================================
        # SAFETY SIGNALS
        # ====================================================

        safety_signals = detect_safety_signals(
            patient=request.patient,
            assessment=request.assessment,
            visit=request.visit,
        )

        # ====================================================
        # CLINICAL CONTEXT
        # ====================================================

        clinical_context = build_clinical_context(
            patient=request.patient,
            assessment=request.assessment,
            visit=request.visit,
            safety_signals=safety_signals,
        )

        # ====================================================
        # TREATMENT ENGINE
        # ====================================================

        patient = request.patient or {}
        assessment = request.assessment or {}
        visit = request.visit or {}

        age = first_value(
            patient,
            "age",
            "age_months",
            default=first_value(
                assessment,
                "age",
                "age_months",
            ),
        )

        age_unit = first_value(
            patient,
            "age_unit",
            default=first_value(
                assessment,
                "age_unit",
                default="months",
            ),
        )

        pneumonia_prediction = first_value(
            assessment,
            "prediction",
            "final_prediction",
            "diagnosis",
            "final_assessment",
        )

        pneumonia_assessment = (
            prediction_is_pneumonia(
                pneumonia_prediction
            )
        )

        fast_breathing = parse_bool(
            first_value(
                assessment,
                "fast_breathing",
                "fast_breathing_present",
                default=first_value(
                    visit,
                    "fast_breathing",
                    "fast_breathing_present",
                ),
            )
        )

        chest_indrawing = safety_signals[
            "chest_indrawing"
        ]

        general_danger_sign = safety_signals[
            "general_danger_sign"
        ]

        spo2 = safety_signals[
            "spo2"
        ]

        treatment_plan = generate_treatment_plan(
            age=age,
            age_unit=age_unit,
            pneumonia_assessment=pneumonia_assessment,
            fast_breathing=fast_breathing,
            chest_indrawing=chest_indrawing,
            general_danger_sign=general_danger_sign,
            spo2=spo2,
        )

        # ====================================================
        # GEMINI
        # ====================================================

        answer = ask_gemini(
            question=request.question,
            language=request.language,
            clinical_context=clinical_context,
            safety_signals=safety_signals,
            treatment_plan=treatment_plan,
        )

        # ====================================================
        # RESPONSE CONTEXT
        # ====================================================

        context_used = {
            "patient": request.patient or {},
            "assessment": request.assessment or {},
            "visit": request.visit or {},
            "clinical_context": clinical_context,
            "safety": safety_signals,
            "treatment_plan": treatment_plan,
        }

        return AssistantChatResponse(
            assistant="PneumoCare AI",
            answer=answer,
            language=request.language,
            safety_flag=safety_signals[
                "safety_flag"
            ],
            safety_message=safety_signals[
                "safety_message"
            ],
            context_used=context_used,
            status="READY",
            treatment_plan=treatment_plan,
        )

    except RuntimeError as exc:

        print(
            "[Assistant] Runtime error:",
            str(exc),
        )

        raise HTTPException(
            status_code=503,
            detail=(
                "The clinical AI assistant could not "
                "get a response from Gemini. "
                f"Gemini is currently unavailable. "
                f"Last error: {exc}"
            ),
        ) from exc

    except Exception as exc:

        print(
            "[Assistant] Unexpected error:",
            str(exc),
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "An unexpected error occurred "
                "inside the clinical AI assistant."
            ),
        ) from exc