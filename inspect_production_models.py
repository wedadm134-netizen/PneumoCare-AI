import json
import os
import joblib

ROOT = os.path.dirname(os.path.abspath(__file__))

FILES = [
    "models/vital_fuse/C_Early_Plus_Imaging.json",
    "models/evidence_fuse_v4/evidence_fuse_v4_config.json",
    "final_package/cbc_v5/cbc_v5_final_inference_spec.json",
    "models/XRay_Branch_V1/xray_branch_manifest.json",
]

print("=" * 70)
print("CAPGuard-AI — PRODUCTION MODEL INSPECTION")
print("=" * 70)

for rel_path in FILES:
    path = os.path.join(ROOT, rel_path)

    print("\n" + "=" * 70)
    print(rel_path)
    print("=" * 70)

    if not os.path.exists(path):
        print("STATUS: NOT FOUND")
        continue

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        text = json.dumps(data, indent=2, ensure_ascii=False)

        if len(text) > 3000:
            text = text[:3000] + "\n...[TRUNCATED]..."

        print(text)

    except Exception as e:
        print("ERROR:", type(e).__name__, str(e))


print("\n" + "=" * 70)
print("CBC MODEL")
print("=" * 70)

cbc_path = os.path.join(
    ROOT,
    "models/cbc/cbc_calibrated_logistic.joblib"
)

try:
    model = joblib.load(cbc_path)

    print("TYPE:", type(model))
    print("N_FEATURES:", getattr(model, "n_features_in_", None))
    print("CLASSES:", getattr(model, "classes_", None))
    print(
        "FEATURE_NAMES:",
        getattr(model, "feature_names_in_", None)
    )

except Exception as e:
    print("ERROR:", type(e).__name__, str(e))


print("\n" + "=" * 70)
print("VITAL PREPROCESSOR")
print("=" * 70)

vital_path = os.path.join(
    ROOT,
    "models/vital_fuse/C_Early_Plus_Imaging_preprocessor.joblib"
)

try:
    preprocessor = joblib.load(vital_path)

    print("TYPE:", type(preprocessor))
    print(
        "N_FEATURES:",
        getattr(preprocessor, "n_features_in_", None)
    )
    print(
        "FEATURE_NAMES:",
        getattr(preprocessor, "feature_names_in_", None)
    )

except Exception as e:
    print("ERROR:", type(e).__name__, str(e))


print("\n" + "=" * 70)
print("INSPECTION COMPLETE")
print("=" * 70)