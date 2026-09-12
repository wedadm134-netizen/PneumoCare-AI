import os
import json
import joblib
import torch
import torch.nn as nn
import numpy as np

from PIL import Image
from torchvision import models, transforms
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path
from huggingface_hub import hf_hub_download


# ============================================================
# CAPGuard AI — Production Model Adapter V1
# ============================================================

PROJECT = os.path.dirname(os.path.abspath(__file__))
MODEL_ROOT = os.path.dirname(PROJECT)

DEVICE = torch.device("cpu")


# ============================================================
# PATHS
# ============================================================

RESNET_PATH = os.getenv("RESNET_PATH", os.path.join(MODEL_ROOT, "models", "resnet50-11ad3fa6.pth"))


XRAY_CHECKPOINT = os.path.join(
    MODEL_ROOT,
    "models",
    "XRay_Branch_V1",
    "model",
    "best_image_classifier.pt"
)

CLINICAL_BERT_DIR = os.path.join(
    MODEL_ROOT,
    "models",
    "clin_note_v4",
    "clinical_bert_v4_final"
)

VITAL_MODEL_PATH = os.path.join(
    MODEL_ROOT,
    "models",
    "vital_fuse",
    "C_Early_Plus_Imaging.json"
)

VITAL_PREPROCESSOR_PATH = os.path.join(
    MODEL_ROOT,
    "models",
    "vital_fuse",
    "C_Early_Plus_Imaging_preprocessor.joblib"
)

FUSION_CONFIG_PATH = os.path.join(
    MODEL_ROOT,
    "models",
    "evidence_fuse_v4",
    "evidence_fuse_v4_config.json"
)


# ============================================================
# CONSTANTS
# ============================================================

XRAY_LABELS = {
    0: "Normal",
    1: "Pneumonia",
}

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
# XRAY CLASSIFIER
# ============================================================

class XRayClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(2048, 512),
            nn.BatchNorm1d(512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 2),
        )
    def forward(self, x):
        return self.network(x)


class CAPGuardModelAdapter:

    def __init__(self):

        self.device = DEVICE

        # Lazy-loading state
        self._models_loaded = False
        self._loading = False

        # Load only lightweight fusion configuration
        self._load_fusion_config()

        # Heavy model placeholders
        self.xray_feature_extractor = None
        self.xray_classifier = None
        self.xray_transform = None

        self.tokenizer = None
        self.nlp_model = None

        self.vital_preprocessor = None
        self.vital_model = None

        print("=" * 70)
        print("CAPGuard AI - MODEL ADAPTER V1")
        print("=" * 70)
        print("CAPGuard ADAPTER: INITIALIZED")
        print("Heavy models will load on first inference.")
        print("=" * 70)

    # ========================================================
    # LAZY MODEL LOADING
    # ========================================================

    def _ensure_models_loaded(self):

        if self._models_loaded:
            return

        if self._loading:
            raise RuntimeError(
                "CAPGuard models are already being loaded."
            )

        self._loading = True

        try:

            print("=" * 70)
            print("CAPGuard AI - Loading production models...")
            print("=" * 70)

            self._load_xray()
            self._load_nlp()
            self._load_vital()

            self._models_loaded = True

            print("CAPGuard ADAPTER: READY")
            print("=" * 70)

        except Exception:

            self._models_loaded = False
            raise

        finally:

            self._loading = False

    # ========================================================
    # FUSION CONFIG
    # ========================================================

    def _load_fusion_config(self):

        with open(
            FUSION_CONFIG_PATH,
            "r",
            encoding="utf-8"
        ) as f:

            self.fusion_config = json.load(f)

        self.nlp_weight = float(
            self.fusion_config["nlp_weight"]
        )

        self.vital_weight = float(
            self.fusion_config["lab_weight"]
        )

        self.fusion_threshold = float(
            self.fusion_config["threshold"]
        )

        print()
        print("[FUSION]")
        print("NLP WEIGHT:", self.nlp_weight)
        print("VITAL WEIGHT:", self.vital_weight)
        print("THRESHOLD:", self.fusion_threshold)

    # ========================================================
    # XRAY
    # ========================================================

    def _load_xray(self):

        print()
        print("[XRAY] Loading ResNet50 ImageNet V2...")

        resnet = models.resnet50(weights=None)

        resnet_path = Path(RESNET_PATH)

        is_lfs_pointer = False
        if resnet_path.is_file():
            try:
                with resnet_path.open("rb") as f:
                    header = f.read(80)
                is_lfs_pointer = header.startswith(b"version https://git-lfs.github.com/spec/v1")
            except Exception:
                is_lfs_pointer = False

        if is_lfs_pointer or not resnet_path.is_file():
            print("[XRAY] ResNet checkpoint not available locally.")
            print("[XRAY] Downloading ResNet50 from Hugging Face...")
            downloaded_resnet = hf_hub_download(
                repo_id="WedadMohamed/PneumoCare-AI-Models",
                filename="resnet50/resnet50-11ad3fa6.pth",
                token=os.getenv("HF_TOKEN"),
            )
            resnet_path = Path(downloaded_resnet)
            print(f"[XRAY] ResNet checkpoint ready: {resnet_path}")

        state = torch.load(
            str(resnet_path),
            map_location="cpu"
        )

        if isinstance(state, dict) and "state_dict" in state:
            state = state["state_dict"]

        state = {
            k.replace("module.", ""): v
            for k, v in state.items()
        }

        resnet.load_state_dict(
            state,
            strict=True
        )

        self.xray_feature_extractor = nn.Sequential(
            *list(resnet.children())[:-1]
        )

        self.xray_feature_extractor.eval()

        self.xray_transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            ),
        ])

        print("[XRAY] ResNet50: OK")

        print("[XRAY] Loading classifier...")

        checkpoint = torch.load(
            XRAY_CHECKPOINT,
            map_location="cpu"
        )

        self.xray_classifier = XRayClassifier()

        if (
            isinstance(checkpoint, dict)
            and "model_state_dict" in checkpoint
        ):

            self.xray_classifier.load_state_dict(
                checkpoint["model_state_dict"],
                strict=True
            )

        elif isinstance(checkpoint, dict):

            self.xray_classifier.load_state_dict(
                checkpoint,
                strict=True
            )

        else:

            raise RuntimeError(
                "Unsupported X-Ray checkpoint format."
            )

        self.xray_classifier.eval()

        print("[XRAY] Classifier: OK")

    # ========================================================
    # CLINICALBERT V4
    # ========================================================

    def _load_nlp(self):

        print()
        print("[NLP] Loading ClinicalBERT V4...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            CLINICAL_BERT_DIR,
            local_files_only=True
        )

        self.nlp_model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                CLINICAL_BERT_DIR,
                local_files_only=True,
                num_labels=2
            )
        )

        self.nlp_model.to(self.device)
        self.nlp_model.eval()

        print("[NLP] ClinicalBERT V4: OK")
        print("[NLP] Max length: 256")
        print("[NLP] Classes: 2")

    # ========================================================
    # VITAL-FUSE
    # ========================================================

    def _load_vital(self):

        print()
        print("[VITAL] Loading preprocessor...")

        self.vital_preprocessor = joblib.load(
            VITAL_PREPROCESSOR_PATH
        )

        print("[VITAL] Preprocessor: OK")

        print("[VITAL] Loading XGBoost model...")

        import xgboost as xgb

        self.vital_model = xgb.XGBClassifier()

        self.vital_model.load_model(
            VITAL_MODEL_PATH
        )

        print("[VITAL] XGBoost: OK")

    # ========================================================
    # XRAY PREDICTION
    # ========================================================

    def predict_xray(self, image_path):

        self._ensure_models_loaded()

        if not image_path:
            raise ValueError(
                "image_path is required for X-Ray inference."
            )

        if not os.path.isfile(image_path):
            raise FileNotFoundError(
                f"X-Ray image not found: {image_path}"
            )

        image = Image.open(
            image_path
        ).convert("RGB")

        x = self.xray_transform(
            image
        ).unsqueeze(0)

        with torch.no_grad():

            features = self.xray_feature_extractor(x)

            features = torch.flatten(
                features,
                1
            )

            logits = self.xray_classifier(
                features
            )

            probabilities = torch.softmax(
                logits,
                dim=1
            )[0]

        normal_probability = float(
            probabilities[0]
        )

        pneumonia_probability = float(
            probabilities[1]
        )

        predicted_index = int(
            torch.argmax(probabilities).item()
        )

        return {
            "available": True,
            "prediction": XRAY_LABELS[predicted_index],
            "class_index": predicted_index,
            "normal_probability": normal_probability,
            "pneumonia_probability": pneumonia_probability,
            "feature_dimension": 2048,
        }

    # ========================================================
    # NLP PREDICTION
    # ========================================================

    def predict_nlp(self, clinical_note):

        self._ensure_models_loaded()

        if (
            not clinical_note
            or not str(clinical_note).strip()
        ):

            raise ValueError(
                "clinical_note is required for NLP inference."
            )

        encoded = self.tokenizer(
            str(clinical_note),
            truncation=True,
            padding=True,
            max_length=256,
            return_tensors="pt",
        )

        encoded = {
            key: value.to(self.device)
            for key, value in encoded.items()
        }

        with torch.no_grad():

            outputs = self.nlp_model(
                **encoded
            )

            probabilities = torch.softmax(
                outputs.logits,
                dim=1
            )[0]

        normal_probability = float(
            probabilities[0]
        )

        pneumonia_probability = float(
            probabilities[1]
        )

        prediction = (
            pneumonia_probability >= 0.65
        )

        return {
            "available": True,
            "prediction": (
                "Pneumonia"
                if prediction
                else "Normal"
            ),
            "class_index": int(prediction),
            "normal_probability": normal_probability,
            "pneumonia_probability": pneumonia_probability,
            "threshold": 0.65,
        }

    # ========================================================
    # VITAL PREDICTION
    # ========================================================

    def predict_vital(self, vital_data):

        self._ensure_models_loaded()

        missing = [
            feature
            for feature in VITAL_RAW_FEATURES
            if feature not in vital_data
        ]

        if missing:

            raise ValueError(
                "Missing VITAL features: "
                + ", ".join(missing)
            )

        row = {
            feature: vital_data[feature]
            for feature in VITAL_RAW_FEATURES
        }

        import pandas as pd

        df = pd.DataFrame(
            [row],
            columns=VITAL_RAW_FEATURES
        )

        transformed = (
            self.vital_preprocessor.transform(df)
        )

        probability = float(
            self.vital_model.predict_proba(
                transformed
            )[0][1]
        )

        prediction = (
            probability >= 0.5
        )

        return {
            "available": True,
            "prediction": (
                "Pneumonia"
                if prediction
                else "Normal"
            ),
            "class_index": int(prediction),
            "pneumonia_probability": probability,
            "normal_probability": 1.0 - probability,
            "raw_feature_count": 47,
            "transformed_feature_count": int(
                transformed.shape[1]
            ),
        }

    # ========================================================
    # FULL PREDICTION
    # ========================================================

    def predict(
        self,
        clinical_note,
        vital_data,
        image_path=None,
    ):

        # ----------------------------------------------------
        # X-Ray
        # ----------------------------------------------------

        xray_result = None

        if image_path:

            xray_result = self.predict_xray(
                image_path
            )

            # ------------------------------------------------
            # Engineering mapping ONLY
            # ------------------------------------------------

            if (
                "chest_xray_finding" not in vital_data
                or vital_data["chest_xray_finding"] is None
            ):

                vital_data = dict(vital_data)

                if xray_result["class_index"] == 1:

                    vital_data[
                        "chest_xray_finding"
                    ] = "Endpoint pneumonia"

                else:

                    vital_data[
                        "chest_xray_finding"
                    ] = "Normal"

        else:

            raise ValueError(
                "Full Evidence-Fuse V4 inference requires "
                "an X-Ray image."
            )

        # ----------------------------------------------------
        # NLP
        # ----------------------------------------------------

        nlp_result = self.predict_nlp(
            clinical_note
        )

        # ----------------------------------------------------
        # VITAL
        # ----------------------------------------------------

        vital_result = self.predict_vital(
            vital_data
        )

        # ----------------------------------------------------
        # Evidence-Fuse V4
        # ----------------------------------------------------

        nlp_probability = (
            nlp_result["pneumonia_probability"]
        )

        vital_probability = (
            vital_result["pneumonia_probability"]
        )

        final_probability = (
            self.nlp_weight * nlp_probability
            +
            self.vital_weight * vital_probability
        )

        final_prediction = (
            final_probability >= self.fusion_threshold
        )

        # ----------------------------------------------------
        # Final result
        # ----------------------------------------------------

        return {
            "engine": "CAPGuard Production Engine V1",
            "status": "SUCCESS",

            "fusion": {
                "method": "weighted_probability_fusion",
                "nlp_weight": self.nlp_weight,
                "vital_weight": self.vital_weight,
                "threshold": self.fusion_threshold,
            },

            "xray": xray_result,

            "nlp": nlp_result,

            "vital": vital_result,

            "final": {
                "prediction": (
                    "Pneumonia"
                    if final_prediction
                    else "Normal"
                ),
                "class_index": int(
                    final_prediction
                ),
                "pneumonia_probability": float(
                    final_probability
                ),
                "normal_probability": float(
                    1.0 - final_probability
                ),
            },
        }


# ============================================================
# SMOKE TEST
# ============================================================

if __name__ == "__main__":

    print()
    print("Initializing CAPGuard adapter...")

    adapter = CAPGuardModelAdapter()

    print()
    print("Adapter initialized successfully.")
    print(
        "Heavy model components will load "
        "when inference is requested."
    )

    print(
        "MODELS_LOADED =",
        adapter._models_loaded
    )

