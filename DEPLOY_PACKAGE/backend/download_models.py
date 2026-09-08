from __future__ import annotations

import os
import shutil
from pathlib import Path

from huggingface_hub import hf_hub_download


# ============================================================
# HUGGING FACE
# ============================================================

REPO_ID = "WedadMohamed/PneumoCare-AI-Models"

HF_TOKEN = os.getenv("HF_TOKEN")


# ============================================================
# PROJECT PATHS
# ============================================================

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parents[1]

ROOT_MODELS = PROJECT_ROOT / "models"
DEPLOY_MODELS = BACKEND_DIR / "models"


# ============================================================
# DOWNLOAD HELPER
# ============================================================

def download_file(repo_path: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)

    print()
    print("=" * 70)
    print(f"Downloading: {repo_path}")
    print(f"Destination: {destination}")
    print("=" * 70)

    downloaded = hf_hub_download(
        repo_id=REPO_ID,
        filename=repo_path,
        token=HF_TOKEN,
    )

    shutil.copy2(downloaded, destination)

    print(f"OK: {destination}")


# ============================================================
# RESNET50
# ============================================================

download_file(
    "resnet50/resnet50-11ad3fa6.pth",
    DEPLOY_MODELS / "resnet50-11ad3fa6.pth",
)


# ============================================================
# X-RAY CLASSIFIER
# ============================================================

download_file(
    "XRay_Branch_V1/best_image_classifier.pt",
    ROOT_MODELS
    / "XRay_Branch_V1"
    / "model"
    / "best_image_classifier.pt",
)


# ============================================================
# CLINICAL BERT V4
# ============================================================

CLINICAL_BERT_FILES = [
    "config.json",
    "model.safetensors",
    "special_tokens_map.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "training_args.bin",
    "vocab.txt",
]

for filename in CLINICAL_BERT_FILES:
    download_file(
        f"clin_note_v4/clinical_bert_v4_final/{filename}",
        ROOT_MODELS
        / "clin_note_v4"
        / "clinical_bert_v4_final"
        / filename,
    )


# ============================================================
# VITAL FUSE
# ============================================================

download_file(
    "vital_fuse/C_Early_Plus_Imaging.json",
    ROOT_MODELS / "vital_fuse" / "C_Early_Plus_Imaging.json",
)

download_file(
    "vital_fuse/C_Early_Plus_Imaging_preprocessor.joblib",
    ROOT_MODELS
    / "vital_fuse"
    / "C_Early_Plus_Imaging_preprocessor.joblib",
)


# ============================================================
# EVIDENCE FUSE V4
# ============================================================

download_file(
    "evidence_fuse_v4/evidence_fuse_v4_config.json",
    ROOT_MODELS
    / "evidence_fuse_v4"
    / "evidence_fuse_v4_config.json",
)


# ============================================================
# VERIFY ALL REQUIRED FILES
# ============================================================

required_files = [
    DEPLOY_MODELS / "resnet50-11ad3fa6.pth",

    ROOT_MODELS
    / "XRay_Branch_V1"
    / "model"
    / "best_image_classifier.pt",

    ROOT_MODELS
    / "clin_note_v4"
    / "clinical_bert_v4_final"
    / "config.json",

    ROOT_MODELS
    / "clin_note_v4"
    / "clinical_bert_v4_final"
    / "model.safetensors",

    ROOT_MODELS
    / "clin_note_v4"
    / "clinical_bert_v4_final"
    / "special_tokens_map.json",

    ROOT_MODELS
    / "clin_note_v4"
    / "clinical_bert_v4_final"
    / "tokenizer.json",

    ROOT_MODELS
    / "clin_note_v4"
    / "clinical_bert_v4_final"
    / "tokenizer_config.json",

    ROOT_MODELS
    / "clin_note_v4"
    / "clinical_bert_v4_final"
    / "training_args.bin",

    ROOT_MODELS
    / "clin_note_v4"
    / "clinical_bert_v4_final"
    / "vocab.txt",

    ROOT_MODELS
    / "vital_fuse"
    / "C_Early_Plus_Imaging.json",

    ROOT_MODELS
    / "vital_fuse"
    / "C_Early_Plus_Imaging_preprocessor.joblib",

    ROOT_MODELS
    / "evidence_fuse_v4"
    / "evidence_fuse_v4_config.json",
]


print()
print("=" * 70)
print("MODEL VERIFICATION")
print("=" * 70)

missing = []

for file_path in required_files:
    if file_path.exists():
        size_mb = file_path.stat().st_size / (1024 * 1024)
        print(f"[OK] {file_path} ({size_mb:.2f} MB)")
    else:
        print(f"[MISSING] {file_path}")
        missing.append(file_path)


print()
print("=" * 70)

if missing:
    print(f"MODEL DOWNLOAD FAILED: {len(missing)} file(s) missing.")
    raise SystemExit(1)

print("ALL PRODUCTION MODELS READY")
print("=" * 70)