import os
import sys
import json
import uuid
import shutil
import tempfile
import psycopg
from psycopg.rows import dict_row
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = Path(__file__).resolve().parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))


# ============================================================
# ASSISTANT API
# ============================================================

from assistant_api import router as assistant_router


# ============================================================
# PRODUCTION AI IMPORTS
# ============================================================

ADAPTER_IMPORT_ERROR = None
ENGINE_IMPORT_ERROR = None

try:
    from capguard_model_adapter import CAPGuardModelAdapter
except Exception as exc:
    CAPGuardModelAdapter = None
    ADAPTER_IMPORT_ERROR = str(exc)

try:
    import capguard_engine
except Exception as exc:
    capguard_engine = None
    ENGINE_IMPORT_ERROR = str(exc)


# ============================================================
# GEMINI SERVICE
# ============================================================

try:
    from gemini_service import generate_clinical_reasoning

    GEMINI_IMPORT_ERROR = None

except Exception as exc:
    generate_clinical_reasoning = None
    GEMINI_IMPORT_ERROR = str(exc)


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CAPGuard AI",
    description="Production Hybrid AI System for Pediatric Community-Acquired Pneumonia",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# DIRECTORIES
# ============================================================

DEPLOY_ROOT = BACKEND_DIR.parent
FRONTEND_DIST = DEPLOY_ROOT / 'frontend' / 'dist'


# ============================================================
# FRONTEND STATIC FILES
# ============================================================

if FRONTEND_DIST.is_dir():
    app.mount(
        "/assets",
        StaticFiles(directory=str(FRONTEND_DIST / "assets")),
        name="frontend-assets",
    )

DATA_DIR = Path(tempfile.gettempdir()) / "pneumocare_data"
UPLOAD_DIR = Path(tempfile.gettempdir()) / "pneumocare_uploads"

DATA_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "capguard.db"



# ============================================================
# DATABASE
# ============================================================

def get_db():
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
    return psycopg.connect(database_url, row_factory=dict_row)

def init_database():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            patient_id SERIAL PRIMARY KEY,
            patient_name TEXT NOT NULL,
            age REAL,
            biological_sex TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS assessments (
            assessment_id SERIAL PRIMARY KEY,
            patient_id INTEGER NOT NULL,
            patient_name TEXT,
            clinical_notes TEXT,
            temperature REAL,
            heart_rate REAL,
            oxygen_saturation REAL,
            xray_path TEXT,
            result_json TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
        )
        """
    )

    conn.commit()
    conn.close()


init_database()


# ============================================================
# MODEL ADAPTER
# ============================================================

MODEL_ADAPTER = None
MODEL_ADAPTER_ERROR = None

if CAPGuardModelAdapter is not None:
    try:
        MODEL_ADAPTER = CAPGuardModelAdapter()
    except Exception as exc:
        MODEL_ADAPTER_ERROR = str(exc)
else:
    MODEL_ADAPTER_ERROR = ADAPTER_IMPORT_ERROR


# ============================================================
# VITAL RAW FEATURES
# ============================================================

VITAL_RAW_FEATURES = [
    "age_months",
    "gender",
    "has_medical_insurance",
    "household_size",
    "num_siblings",
    "num_rooms_in_house",
    "smokers_at_home",
    "tb_contact",
    "prior_respiratory_admission",
    "prematurity",
    "breastfeeding",
    "vaccinations_age_appropriate",
    "hib_vaccine_doses",
    "pneumococcal_vaccine_doses",
    "rotavirus_vaccine_doses",
    "vitamin_a_supplementation",
    "prior_antibiotic_use_2weeks",
    "known_asthmatic",
    "chronic_condition",
    "pain_duration_before_consult_days",
    "history_fever",
    "days_with_fever",
    "history_vomiting",
    "history_diarrhea",
    "history_cough",
    "history_rhinorrhea",
    "weight_kg",
    "height_cm",
    "unusual_sleepiness",
    "spo2_pct",
    "temperature_c",
    "respiratory_rate",
    "heart_rate",
    "paleness",
    "disorders_of_consciousness",
    "dehydration_signs",
    "restlessness",
    "cyanosis",
    "nasal_flaring",
    "laryngeal_stridor",
    "rhonchi",
    "crackles",
    "wheezing",
    "hypoventilation",
    "nasopharyngeal_aspiration",
    "bmi",
    "chest_xray_finding",
]


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class PatientCreate(BaseModel):
    patient_name: str = Field(..., min_length=1)
    age: Optional[float] = None
    biological_sex: Optional[str] = None


class AssessmentInput(BaseModel):
    patient_id: int

    patient_name: Optional[str] = None
    age: Optional[float] = None
    biological_sex: Optional[str] = None

    temperature: Optional[float] = None
    heart_rate: Optional[float] = None
    oxygen_saturation: Optional[float] = None

    clinical_notes: Optional[str] = None

    lab_data: Optional[Dict[str, Any]] = None
    cbc_data: Optional[Dict[str, Any]] = None

    xray_path: Optional[str] = None


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def now_iso() -> str:
    return datetime.utcnow().isoformat() + "Z"


def json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            str(key): json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]

    try:
        import numpy as np

        if isinstance(value, np.ndarray):
            return value.tolist()

        if isinstance(value, np.generic):
            return value.item()

    except Exception:
        pass

    try:
        import torch

        if isinstance(value, torch.Tensor):
            return value.detach().cpu().tolist()

    except Exception:
        pass

    if isinstance(value, (str, int, float, bool)) or value is None:
        return value

    return str(value)


def normalize_sex(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None

    value = str(value).strip().lower()

    if value in {"male", "m", "boy"}:
        return "Male"

    if value in {"female", "f", "girl"}:
        return "Female"

    return str(value).strip()


def get_patient(patient_id: int):
    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM patients
            WHERE patient_id = %s
            """,
            (patient_id,),
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        conn.close()


def resolve_xray_path(
    patient_id: int,
    requested_path: Optional[str] = None,
) -> Optional[Path]:

    if requested_path:
        path = Path(requested_path)

        if not path.is_absolute():
            path = PROJECT_ROOT / path

        path = path.resolve()

        if not path.is_file():
            raise HTTPException(
                status_code=404,
                detail="Requested X-ray file was not found.",
            )

        return path

    patient_dir = UPLOAD_DIR / f"patient_{patient_id}"

    if not patient_dir.exists():
        return None

    image_files = []

    for pattern in [
        "*.png",
        "*.jpg",
        "*.jpeg",
        "*.webp",
    ]:
        image_files.extend(patient_dir.glob(pattern))

    image_files = [
        path
        for path in image_files
        if path.is_file()
    ]

    if not image_files:
        return None

    image_files.sort(
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )

    return image_files[0]


# ============================================================
# VITAL DATA BUILDER
# ============================================================

def build_vital_data(
    data: AssessmentInput,
    xray_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    vital_data = dict(data.lab_data or {})

    if data.age is not None:
        vital_data["age_months"] = float(data.age) * 12.0

    if data.biological_sex is not None:
        vital_data["gender"] = normalize_sex(
            data.biological_sex
        )

    if data.temperature is not None:
        vital_data["temperature_c"] = data.temperature

    if data.heart_rate is not None:
        vital_data["heart_rate"] = data.heart_rate

    if data.oxygen_saturation is not None:
        vital_data["spo2_pct"] = data.oxygen_saturation

    if (
        not vital_data.get("chest_xray_finding")
        and xray_result
    ):
        prediction = str(
            xray_result.get("prediction", "")
        ).lower()

        if prediction == "pneumonia":
            vital_data["chest_xray_finding"] = (
                "Endpoint pneumonia"
            )

        elif prediction == "normal":
            vital_data["chest_xray_finding"] = "Normal"

    return {
        feature: vital_data.get(feature)
        for feature in VITAL_RAW_FEATURES
    }


# ============================================================
# SEVERITY INPUT BUILDER
# ============================================================

def build_severity_inputs(
    vital_data: Dict[str, Any],
) -> Dict[str, Any]:

    def as_bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        if isinstance(value, (int, float)):
            return value != 0

        text = str(value).strip().lower()

        return text in {
            "true",
            "yes",
            "y",
            "1",
            "positive",
            "present",
        }

    respiratory_distress_fields = [
        "nasal_flaring",
        "laryngeal_stridor",
        "rhonchi",
        "crackles",
        "wheezing",
        "hypoventilation",
    ]

    distress_count = sum(
        1
        for field in respiratory_distress_fields
        if as_bool(vital_data.get(field))
    )

    spo2 = vital_data.get("spo2_pct")

    try:
        spo2 = float(spo2) if spo2 is not None else None
    except Exception:
        spo2 = None

    return {
        "spo2": spo2,
        "cyanosis": as_bool(
            vital_data.get("cyanosis")
        ),
        "altered_consciousness": as_bool(
            vital_data.get("disorders_of_consciousness")
        ),
        "hypoventilation": as_bool(
            vital_data.get("hypoventilation")
        ),
        "respiratory_distress_count": distress_count,
        "radiologic_complication": False,
        "tachypnea": False,
        "single_respiratory_distress": distress_count == 1,
        "unusual_sleepiness": as_bool(
            vital_data.get("unusual_sleepiness")
        ),
        "dehydration": as_bool(
            vital_data.get("dehydration_signs")
        ),
        "restlessness": as_bool(
            vital_data.get("restlessness")
        ),
    }


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/favicon.svg")
def favicon():
    return FileResponse(str(FRONTEND_DIST / "favicon.svg"))


@app.get("/icons.svg")
def icons():
    return FileResponse(str(FRONTEND_DIST / "icons.svg"))

@app.get("/")
def root():
    if FRONTEND_DIST.is_dir():
        return FileResponse(str(FRONTEND_DIST / "index.html"))

    return {
        "project": "PneumoCare AI",
        "status": "READY" if MODEL_ADAPTER is not None and capguard_engine is not None else "NOT_READY",
        "api": "FastAPI",
        "version": "1.0.0",
    }

# ============================================================
# XAI / GRAD-CAM
# ============================================================

@app.get("/api/xai/{filename}")
def get_xai_image(filename: str):

    xai_dir = (
        Path(__file__).resolve().parent.parent.parent
        / "reports"
        / "xai"
        / "xray_gradcam_v1"
    )

    file_path = xai_dir / filename

    try:
        file_path = file_path.resolve()
        xai_dir = xai_dir.resolve()

        if xai_dir not in file_path.parents:
            raise HTTPException(
                status_code=400,
                detail="Invalid XAI file path.",
            )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid XAI file path.",
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Grad-CAM image not found.",
        )

    return FileResponse(
        path=str(file_path),
        media_type="image/png",
        filename=file_path.name,
    )


# ============================================================
# HEALTH
# ============================================================

@app.get("/api/health")
def health():

    adapter_ready = MODEL_ADAPTER is not None
    engine_ready = capguard_engine is not None
    gemini_ready = generate_clinical_reasoning is not None

    status = (
        "healthy"
        if adapter_ready and engine_ready
        else "degraded"
    )

    return {
        "project": "CAPGuard AI",
        "status": status,
        "adapter": {
            "ready": adapter_ready,
            "error": MODEL_ADAPTER_ERROR,
        },
        "engine": {
            "ready": engine_ready,
            "version": (
                capguard_engine.ENGINE_VERSION
                if engine_ready
                else None
            ),
            "error": (
                None
                if engine_ready
                else ENGINE_IMPORT_ERROR
            ),
        },
        "gemini": {
            "ready": gemini_ready,
            "provider": "Google Gemini",
            "model": os.getenv(
                "GEMINI_MODEL",
                "gemini-3.7-flash",
            ),
            "error": GEMINI_IMPORT_ERROR,
        },
        "timestamp": now_iso(),
    }


# ============================================================
# MODEL STATUS
# ============================================================

@app.get("/api/models/status")
def models_status():

    if capguard_engine is None:
        return {
            "status": "UNAVAILABLE",
            "adapter_ready": MODEL_ADAPTER is not None,
            "gemini_ready": (
                generate_clinical_reasoning is not None
            ),
            "engine_error": ENGINE_IMPORT_ERROR,
        }

    try:
        status = capguard_engine.system_status()
        status = json_safe(status)

    except Exception as exc:
        status = {
            "status": "ERROR",
            "error": str(exc),
        }

    status["gemini"] = {
        "ready": generate_clinical_reasoning is not None,
        "provider": "Google Gemini",
        "model": os.getenv(
            "GEMINI_MODEL",
            "gemini-3.7-flash",
        ),
        "error": GEMINI_IMPORT_ERROR,
    }

    return status


# ============================================================
# CONFIGURATION
# ============================================================

@app.get("/api/configuration")
def configuration():

    return {
        "project": "CAPGuard AI",
        "release": "Production Release V1",
        "fusion": {
            "method": "weighted_probability_fusion",
            "nlp_weight": 0.73,
            "vital_weight": 0.27,
            "threshold": 0.665,
        },
        "models": {
            "xray": "XRay_Branch_V1",
            "text": "CLIN-NOTE V4",
            "structured": "VITAL-FUSE",
            "fusion": "Evidence-Fuse V4",
        },
        "generative_layer": {
            "provider": "Google Gemini",
            "model": os.getenv(
                "GEMINI_MODEL",
                "gemini-3.7-flash",
            ),
            "role": "Clinical Explanation Only",
            "overrides_capguard": False,
        },
        "xray": {
            "backbone": "ResNet50",
            "classifier": "Production Image Classifier",
            "feature_dimension": 2048,
            "input_size": "224x224",
            "classes": [
                "Normal",
                "Pneumonia",
            ],
        },
        "text": {
            "model": "Bio_ClinicalBERT",
            "max_length": 256,
            "classes": [
                "Normal",
                "Pneumonia",
            ],
            "decision_threshold": 0.65,
        },
        "vital": {
            "raw_features": 47,
            "transformed_features": 81,
            "model": "XGBoost",
        },
        "safety": {
            "xray_included_in_fusion": False,
            "gemini_overrides_result": False,
        },
        "cbc": {
            "available": True,
            "optional_input": True,
            "currently_used_in_evidence_fuse_v4": False,
        },
    }


# ============================================================
# PATIENT APIs
# ============================================================

@app.post("/api/patients")
def create_patient(data: PatientCreate):

    patient_name = data.patient_name.strip()

    if not patient_name:
        raise HTTPException(
            status_code=400,
            detail="Patient name is required.",
        )

    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO patients (
                patient_name,
                age,
                biological_sex,
                created_at
            )
            VALUES (%s, %s, %s, %s)
            """,
            (
                patient_name,
                data.age,
                normalize_sex(data.biological_sex),
                now_iso(),
            ),
        )

        cursor.execute("SELECT lastval() AS patient_id")
        patient_id = cursor.fetchone()['patient_id']

        conn.commit()

    finally:
        conn.close()

    return {
        "status": "success",
        "patient": {
            "patient_id": patient_id,
            "patient_name": patient_name,
            "age": data.age,
            "biological_sex": normalize_sex(
                data.biological_sex
            ),
        },
    }


@app.get("/api/patients")
def list_patients():

    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM patients
            ORDER BY patient_id DESC
            """
        )

        rows = cursor.fetchall()

        patients = [
            dict(row)
            for row in rows
        ]

    finally:
        conn.close()

    return {
        "status": "success",
        "patients": patients,
        "count": len(patients),
    }


@app.get("/api/patients/{patient_id}")
def get_patient_by_id(patient_id: int):

    patient = get_patient(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found.",
        )

    return {
        "status": "success",
        "patient": patient,
    }


# ============================================================
# X-RAY UPLOAD
# ============================================================

@app.post("/api/patients/{patient_id}/xray")
async def upload_xray(
    patient_id: int,
    file: UploadFile = File(...),
):

    patient = get_patient(patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found.",
        )

    original_filename = file.filename or ""

    extension = Path(
        original_filename
    ).suffix.lower()

    allowed_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
    }

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported X-ray format. "
                "Allowed formats: PNG, JPG, JPEG, WEBP. "
                "DICOM is not enabled."
            ),
        )

    patient_dir = UPLOAD_DIR / f"patient_{patient_id}"
    patient_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    unique_id = uuid.uuid4().hex[:8]

    filename = (
        f"{timestamp}_{unique_id}{extension}"
    )

    saved_path = patient_dir / filename

    with saved_path.open("wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return {
        "status": "success",
        "patient_id": patient_id,
        "original_filename": original_filename,
        "saved_path": str(saved_path),
        "xray_path": str(saved_path),
    }


# ============================================================
# PRODUCTION ASSESSMENT
# ============================================================

@app.post("/api/assessment")
def run_assessment(
    data: AssessmentInput,
):

    if MODEL_ADAPTER is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "CAPGuard model adapter is unavailable."
            ),
        )

    if capguard_engine is None:
        raise HTTPException(
            status_code=503,
            detail=(
                "CAPGuard production engine is unavailable."
            ),
        )

    patient = get_patient(data.patient_id)

    if patient is None:
        raise HTTPException(
            status_code=404,
            detail="Patient not found.",
        )

    clinical_note = (
        data.clinical_notes or ""
    ).strip()

    if not clinical_note:
        raise HTTPException(
            status_code=400,
            detail="Clinical notes are required.",
        )

    xray_path = resolve_xray_path(
        data.patient_id,
        data.xray_path,
    )

    if xray_path is None:
        raise HTTPException(
            status_code=400,
            detail=(
                "X-ray image is required before "
                "running the assessment."
            ),
        )

    allowed_extensions = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
    }

    if xray_path.suffix.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Unsupported X-ray file format.",
        )

    errors: Dict[str, Any] = {}

    # --------------------------------------------------------
    # X-RAY BRANCH
    # --------------------------------------------------------

    try:
        xray_result = MODEL_ADAPTER.predict_xray(
            str(xray_path)
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"X-ray inference failed: {exc}",
        )

    # --------------------------------------------------------
    # VITAL BRANCH
    # --------------------------------------------------------

    vital_data = build_vital_data(
        data,
        xray_result,
    )

    try:
        vital_result = MODEL_ADAPTER.predict_vital(
            vital_data
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"VITAL inference failed: {exc}",
        )

    # --------------------------------------------------------
    # CLINICAL NLP BRANCH
    # --------------------------------------------------------

    try:
        nlp_result = MODEL_ADAPTER.predict_nlp(
            clinical_note
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Clinical NLP inference failed: {exc}",
        )

    # --------------------------------------------------------
    # EVIDENCE FUSION
    # --------------------------------------------------------

    try:
        fusion_result = (
            capguard_engine.evidence_fuse_v4(
                clinical_result=nlp_result,
                vital_result=vital_result,
            )
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Evidence fusion failed: {exc}",
        )

    # --------------------------------------------------------
    # SEVERITY
    # --------------------------------------------------------

    severity_inputs = build_severity_inputs(
        vital_data
    )

    try:
        severity_result = (
            capguard_engine.severity_assessment(
                **severity_inputs
            )
        )

    except Exception as exc:
        severity_result = {
            "status": "ERROR",
            "error": str(exc),
        }

        errors["severity"] = str(exc)

    # --------------------------------------------------------
    # TREATMENT GUIDANCE
    # --------------------------------------------------------

    severity_value = (
        severity_result.get("severity")
        or severity_result.get("risk_level")
        or "LOW"
    )

    bacterial_probability = (
        fusion_result.get(
            "pneumonia_probability"
        )
    )

    try:
        treatment_result = (
            capguard_engine.treatment_guidance(
                severity=severity_value,
                bacterial_probability=bacterial_probability,
                radiologic_complication=None,
            )
        )

    except Exception as exc:
        treatment_result = {
            "status": "ERROR",
            "error": str(exc),
        }

        errors["treatment"] = str(exc)

    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    final_probability = fusion_result.get(
        "pneumonia_probability"
    )

    final_prediction = fusion_result.get(
        "prediction"
    )

    if final_probability is None:
        raise HTTPException(
            status_code=500,
            detail=(
                "Fusion engine did not return "
                "a pneumonia probability."
            ),
        )

    try:
        final_probability = float(
            final_probability
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Invalid pneumonia probability returned by fusion engine.",
        )

    # --------------------------------------------------------
    # GRAD-CAM
    # --------------------------------------------------------

    xai_result: Dict[str, Any]

    try:
        from web_app.backend.xray_xai import (
            generate_production_gradcam
        )

        xai_dir = (
            Path(__file__).resolve().parent.parent.parent
            / "reports"
            / "xai"
            / "xray_gradcam_v1"
        )

        xai_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        xai_filename = (
            f"patient_{data.patient_id}_"
            f"{uuid.uuid4().hex[:12]}_gradcam.png"
        )

        xai_output_path = (
            xai_dir / xai_filename
        )

        generate_production_gradcam(
            adapter=MODEL_ADAPTER,
            image_path=str(xray_path),
            output_path=xai_output_path,
        )

        xai_result = {
            "available": True,
            "method": "Grad-CAM",
            "model": "ResNet50 ImageNet V2",
            "target_layer": "ResNet50.layer4",
            "filename": xai_filename,
            "url": f"/api/xai/{xai_filename}",
        }

    except Exception as exc:
        errors["xai"] = str(exc)

        xai_result = {
            "available": False,
            "method": "Grad-CAM",
            "model": "ResNet50 ImageNet V2",
            "target_layer": "ResNet50.layer4",
            "error": str(exc),
        }

    # --------------------------------------------------------
    # DECISION EXPLANATION
    # --------------------------------------------------------

    try:
        clinical_probability = float(
            nlp_result.get(
                "pneumonia_probability",
                0.0,
            )
        )
    except Exception:
        clinical_probability = 0.0

    try:
        vital_probability = float(
            vital_result.get(
                "pneumonia_probability",
                0.0,
            )
        )
    except Exception:
        vital_probability = 0.0

    try:
        xray_probability = float(
            xray_result.get(
                "pneumonia_probability",
                0.0,
            )
        )
    except Exception:
        xray_probability = 0.0

    fusion_weights = fusion_result.get(
        "weights",
        {},
    )

    clinical_weight = float(
        fusion_weights.get(
            "nlp_weight",
            0.73,
        )
    )

    vital_weight = float(
        fusion_weights.get(
            "vital_weight",
            0.27,
        )
    )

    fusion_threshold = float(
        fusion_result.get(
            "threshold",
            0.665,
        )
    )

    calculated_probability = (
        clinical_weight * clinical_probability
        + vital_weight * vital_probability
    )

    xray_prediction = xray_result.get(
        "prediction"
    )

    conflict = (
        xray_prediction is not None
        and final_prediction is not None
        and str(xray_prediction).lower()
        != str(final_prediction).lower()
    )

    decision_explanation = {
        "final_prediction": final_prediction,
        "overall_risk": final_probability,
        "threshold": fusion_threshold,
        "contributors": {
            "clinical_nlp": {
                "probability": clinical_probability,
                "weight": clinical_weight,
            },
            "vital": {
                "probability": vital_probability,
                "weight": vital_weight,
            },
            "xray": {
                "probability": xray_probability,
                "included_in_fusion": False,
            },
        },
        "calculation": {
            "formula": (
                f"({clinical_weight:.2f} x "
                f"{clinical_probability:.4f}) + "
                f"({vital_weight:.2f} x "
                f"{vital_probability:.4f})"
            ),
            "calculated_probability": (
                calculated_probability
            ),
            "matches_engine_probability": (
                abs(
                    calculated_probability
                    - final_probability
                )
                < 0.01
            ),
        },
        "xray_evidence": {
            "prediction": xray_prediction,
            "probability": xray_probability,
            "included_in_fusion": False,
        },
        "conflict": {
            "detected": conflict,
            "xray_prediction": xray_prediction,
            "final_prediction": final_prediction,
        },
        "interpretation": (
            "Final decision is produced by the "
            "production Evidence-Fuse V4 layer using "
            "clinical NLP and VITAL evidence. "
            "The X-ray branch provides independent "
            "radiologic evidence and explainability."
        ),
    }

    # --------------------------------------------------------
    # COMPLETE RESULT
    # --------------------------------------------------------

    result = {
        "engine": "CAPGuard Production Engine V1",
        "status": "success",

        "patient": {
            "patient_id": patient["patient_id"],
            "patient_name": (
                data.patient_name
                or patient["patient_name"]
            ),
            "age": (
                data.age
                if data.age is not None
                else patient["age"]
            ),
            "biological_sex": (
                normalize_sex(
                    data.biological_sex
                )
                if data.biological_sex is not None
                else patient["biological_sex"]
            ),
        },

        "result": {
            "prediction": final_prediction,
            "pneumonia_probability": final_probability,
            "normal_probability": (
                1.0 - final_probability
            ),
        },

        "fusion": fusion_result,

        "decision_explanation": decision_explanation,

        "xai": xai_result,

        "branches": {
            "xray": xray_result,
            "clinical_nlp": nlp_result,
            "vital": vital_result,
        },

        "severity": severity_result,

        "treatment": treatment_result,

        "modalities": {
            "xray": True,
            "clinical_notes": True,
            "vital": True,
            "cbc": bool(data.cbc_data),
        },

        "production_models": {
            "xray": "XRay_Branch_V1",
            "clinical_notes": "CLIN-NOTE V4",
            "vital": "VITAL-FUSE",
            "fusion": "Evidence-Fuse V4",
        },

        "errors": errors,

        "timestamp": now_iso(),
    }

    result = json_safe(result)

    # --------------------------------------------------------
    # GEMINI CLINICAL REASONING
    # --------------------------------------------------------

    if generate_clinical_reasoning is not None:

        try:
            gemini_result = (
                generate_clinical_reasoning(
                    result
                )
            )

        except Exception as exc:

            gemini_result = {
                "status": "UNAVAILABLE",
                "provider": "Google Gemini",
                "model": os.getenv(
                    "GEMINI_MODEL",
                    "gemini-3.7-flash",
                ),
                "error": str(exc),
                "reasoning": None,
            }

            errors["gemini"] = str(exc)

    else:

        gemini_result = {
            "status": "UNAVAILABLE",
            "provider": "Google Gemini",
            "model": os.getenv(
                "GEMINI_MODEL",
                "gemini-3.7-flash",
            ),
            "error": GEMINI_IMPORT_ERROR,
            "reasoning": None,
        }

        errors["gemini"] = GEMINI_IMPORT_ERROR

    result["ai_clinical_reasoning"] = json_safe(
        gemini_result
    )

    result["errors"] = errors

    # --------------------------------------------------------
    # SAVE ASSESSMENT
    # --------------------------------------------------------

    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO assessments (
                patient_id,
                patient_name,
                clinical_notes,
                temperature,
                heart_rate,
                oxygen_saturation,
                xray_path,
                result_json,
                created_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data.patient_id,
                data.patient_name
                or patient["patient_name"],
                clinical_note,
                data.temperature,
                data.heart_rate,
                data.oxygen_saturation,
                str(xray_path),
                json.dumps(
                    result,
                    ensure_ascii=False,
                ),
                now_iso(),
            ),
        )

        conn.commit()

    finally:
        conn.close()

    return result


# ============================================================
# PATIENT HISTORY
# ============================================================

@app.get("/api/history/{patient_id}")
def get_patient_history(patient_id: int):
    patient = get_patient(patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found.")

    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                assessment_id,
                patient_id,
                patient_name,
                clinical_notes,
                temperature,
                heart_rate,
                oxygen_saturation,
                xray_path,
                result_json,
                created_at
            FROM assessments
            WHERE patient_id = %s
            ORDER BY assessment_id DESC
        """, (patient_id,))
        rows = cursor.fetchall()
    finally:
        conn.close()

    history = []

    for row in rows:
        raw_result = row["result_json"]

        try:
            parsed = json.loads(raw_result)
        except Exception:
            parsed = {"result": raw_result}

        if not isinstance(parsed, dict):
            parsed = {"result": parsed}

        # Keep the original frontend-compatible structure.
        item = {
            "assessment_id": row["assessment_id"],
            "patient_id": row["patient_id"],
            "patient_name": row["patient_name"],
            "clinical_notes": row["clinical_notes"],
            "temperature": row["temperature"],
            "heart_rate": row["heart_rate"],
            "oxygen_saturation": row["oxygen_saturation"],
            "xray_path": row["xray_path"],
            "created_at": row["created_at"],
            "result": parsed.get("result", {}),
            "fusion": parsed.get("fusion"),
            "severity": parsed.get("severity"),
            "treatment": parsed.get("treatment"),
            "ai_clinical_reasoning": parsed.get("ai_clinical_reasoning"),
            "xai": parsed.get("xai"),
            "xray": parsed.get("branches", {}).get("xray"),
            "clinical_nlp": parsed.get("branches", {}).get("clinical_nlp"),
            "vital": parsed.get("branches", {}).get("vital"),
            "decision_explanation": parsed.get("decision_explanation"),
            "modalities": parsed.get("modalities"),
            "production_models": parsed.get("production_models"),
            "errors": parsed.get("errors", {}),
            "timestamp": parsed.get("timestamp"),
            "full_assessment": parsed,
        }

        history.append(item)

    return {
        "status": "success",
        "patient": patient,
        "history": history,
        "count": len(history),
    }


# ============================================================
# ALL HISTORY
# ============================================================

@app.get("/api/history")
def get_all_history():

    conn = get_db()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                assessment_id,
                patient_id,
                patient_name,
                clinical_notes,
                temperature,
                heart_rate,
                oxygen_saturation,
                xray_path,
                result_json,
                created_at
            FROM assessments
            ORDER BY assessment_id DESC
            """
        )

        rows = cursor.fetchall()

    finally:
        conn.close()

    history = []

    for row in rows:

        raw_result = row["result_json"]

        try:
            result_json = json.loads(
                raw_result
            )
        except Exception:
            result_json = raw_result

        history.append(
            {
                "assessment_id": row[
                    "assessment_id"
                ],
                "patient_id": row[
                    "patient_id"
                ],
                "patient_name": row[
                    "patient_name"
                ],
                "clinical_notes": row[
                    "clinical_notes"
                ],
                "temperature": row[
                    "temperature"
                ],
                "heart_rate": row[
                    "heart_rate"
                ],
                "oxygen_saturation": row[
                    "oxygen_saturation"
                ],
                "xray_path": row[
                    "xray_path"
                ],
                "created_at": row[
                    "created_at"
                ],
                "result": result_json,
            }
        )

    return {
        "status": "success",
        "history": history,
        "count": len(history),
    }


# ============================================================
# ASSISTANT ROUTER
# ============================================================

app.include_router(assistant_router)


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 78)
    print("CAPGuard-AI - PRODUCTION BACKEND V1")
    print("=" * 78)

    print(f"PROJECT ROOT : {PROJECT_ROOT}")
    print(f"BACKEND DIR  : {BACKEND_DIR}")
    print(f"DATABASE     : {DB_PATH}")
    print(f"UPLOAD DIR   : {UPLOAD_DIR}")

    print("-" * 78)

    if MODEL_ADAPTER is not None:
        print("CAPGuard ADAPTER: READY")
    else:
        print("CAPGuard ADAPTER: ERROR")
        print(f"ERROR: {MODEL_ADAPTER_ERROR}")

    if capguard_engine is not None:
        print("CAPGuard ENGINE : READY")
    else:
        print("CAPGuard ENGINE : ERROR")
        print(f"ERROR: {ENGINE_IMPORT_ERROR}")

    if generate_clinical_reasoning is not None:
        print("GEMINI SERVICE  : READY")
        print(
            "GEMINI MODEL    : "
            f"{os.getenv('GEMINI_MODEL', 'gemini-3.7-flash')}"
        )
    else:
        print("GEMINI SERVICE  : UNAVAILABLE")
        print(f"ERROR: {GEMINI_IMPORT_ERROR}")

    print("-" * 78)

    print("Production Fusion:")
    print("  NLP   Weight : 0.73")
    print("  VITAL Weight : 0.27")
    print("  Threshold    : 0.665")

    print("-" * 78)

    print("Models:")
    print("  X-Ray  : XRay_Branch_V1")
    print("  Text   : CLIN-NOTE V4")
    print("  VITAL  : VITAL-FUSE")
    print("  Fusion : Evidence-Fuse V4")

    print("-" * 78)

    print("Generative Layer:")
    print("  Provider : Google Gemini")
    print(
        "  Model    : "
        f"{os.getenv('GEMINI_MODEL', 'gemini-3.7-flash')}"
    )
    print("  Role     : Clinical Explanation Only")
    print("  Overrides CAPGuard: NO")

    print("=" * 78)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app,
        host='0.0.0.0',
        port=int(os.getenv('PORT', '8000')),
        reload=False,
    )
