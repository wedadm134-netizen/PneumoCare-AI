import os
import json
import pandas as pd

from capguard_model_adapter import CAPGuardModelAdapter


PROJECT = r"C:\Users\hp\Desktop\CAPGuard-AI"

TRAIN_CSV = os.path.join(
    PROJECT,
    r"data\master_train.csv"
)

XAI_DIR = os.path.join(
    PROJECT,
    r"final_package\XRay_Branch_V1\xai"
)


# ============================================================
# FIND TEST X-RAY
# ============================================================

image_path = None

for root, dirs, files in os.walk(XAI_DIR):
    for f in files:
        if f.lower().endswith("_original.png"):
            image_path = os.path.join(root, f)
            break

    if image_path:
        break


if image_path is None:
    raise FileNotFoundError(
        "No X-Ray image found."
    )


print("=" * 70)
print("CAPGuard AI — FULL LIVE INFERENCE TEST")
print("=" * 70)

print()
print("X-RAY:")
print(image_path)


# ============================================================
# LOAD ONE REAL VITAL ROW
# ============================================================

df = pd.read_csv(TRAIN_CSV)

if len(df) == 0:
    raise RuntimeError(
        "master_train.csv is empty."
    )


row = df.iloc[0]


# ============================================================
# CONVERT ROW TO VITAL DICT
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


vital_data = {}

for feature in VITAL_RAW_FEATURES:

    value = row[feature]

    if pd.isna(value):
        value = None

    vital_data[feature] = value


# ============================================================
# CLINICAL NOTE
# ============================================================

clinical_note = (
    "Child presents with fever and cough. "
    "Respiratory symptoms are reported with "
    "increased work of breathing. "
    "No diagnosis or imaging interpretation is included "
    "in the clinical narrative."
)


# ============================================================
# ADAPTER
# ============================================================

adapter = CAPGuardModelAdapter()


# ============================================================
# FULL PREDICTION
# ============================================================

result = adapter.predict(
    clinical_note=clinical_note,
    vital_data=vital_data,
    image_path=image_path,
)


# ============================================================
# OUTPUT
# ============================================================

print()
print("=" * 70)
print("FINAL CAPGuard RESULT")
print("=" * 70)

print(
    json.dumps(
        result,
        indent=2,
        ensure_ascii=False
    )
)

print()
print("=" * 70)
print("FULL LIVE INFERENCE: SUCCESS")
print("=" * 70)