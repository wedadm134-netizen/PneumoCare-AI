from pathlib import Path
import shutil

SOURCE = Path("assistant_api.py")
BACKUP = Path("assistant_api_backup_before_treatment_v2.py")

print("=" * 70)
print("PneumoCare AI — Assistant Treatment Integration Patch")
print("=" * 70)

if not SOURCE.exists():
    raise FileNotFoundError("assistant_api.py was not found.")

# Create an additional backup before modifying anything.
shutil.copy2(SOURCE, BACKUP)
print(f"Backup created: {BACKUP}")

text = SOURCE.read_text(encoding="utf-8")

# -------------------------------------------------------------------
# 1. Add Treatment Engine import
# -------------------------------------------------------------------
old = "from typing import Optional, Dict, Any"

new = """from typing import Optional, Dict, Any

from treatment_engine import generate_treatment_plan"""

if "from treatment_engine import generate_treatment_plan" not in text:
    if old not in text:
        raise RuntimeError("Import insertion point was not found.")
    text = text.replace(old, new, 1)

# -------------------------------------------------------------------
# 2. Add treatment_plan to response model
# -------------------------------------------------------------------
old = """    context_used: Dict[str, Any]
    status: str"""

new = """    context_used: Dict[str, Any]
    status: str
    treatment_plan: Optional[Dict[str, Any]] = None"""

if "treatment_plan: Optional[Dict[str, Any]] = None" not in text:
    if old not in text:
        raise RuntimeError("Response model insertion point was not found.")
    text = text.replace(old, new, 1)

# -------------------------------------------------------------------
# 3. Insert treatment-engine processing before context
# -------------------------------------------------------------------
marker = "    context = {"

if "Treatment Engine Integration" not in text:

    treatment_block = """    # ------------------------------------------------------------
    # Treatment Engine Integration
    # ------------------------------------------------------------

    def first_value(*keys):
        for source in (assessment, request.visit or {}):
            for key in keys:
                value = source.get(key)
                if value is not None:
                    return value
        return None

    age = patient.get("age")
    age_unit = patient.get("age_unit", "years")

    fast_breathing = bool(first_value(
        "fast_breathing",
        "fastBreathing",
        "tachypnea",
    ))

    chest_indrawing = bool(first_value(
        "chest_indrawing",
        "chestIndrawing",
    ))

    general_danger_sign = bool(first_value(
        "general_danger_sign",
        "danger_sign",
        "danger_signs",
    ))

    spo2 = first_value(
        "spo2",
        "SpO2",
        "oxygen_saturation",
        "oxygen_saturation_percent",
    )

    prediction_text = str(prediction or "").strip().lower()

    pneumonia_assessment = (
        "pneumonia" in prediction_text
        and "no pneumonia" not in prediction_text
    )

    treatment_plan = generate_treatment_plan(
        age=age,
        age_unit=age_unit,
        pneumonia_assessment=pneumonia_assessment,
        fast_breathing=fast_breathing,
        chest_indrawing=chest_indrawing,
        general_danger_sign=general_danger_sign,
        spo2=spo2,
    )

"""

    if marker not in text:
        raise RuntimeError("Context insertion point was not found.")

    text = text.replace(marker, treatment_block + marker, 1)

# -------------------------------------------------------------------
# 4. Replace medication refusal with treatment-engine response
# -------------------------------------------------------------------
old_start = """    elif safety["medication_request"]:

        if request.language == "ar":
            message = ("""

new_block = """    elif safety["medication_request"]:

        if treatment_plan["status"] == "RECOMMENDED":

            medicines = ", ".join(
                treatment_plan["antimicrobial_options"]
            )

            if request.language == "ar":
                message = (
                    "الخطة العلاجية المقترحة حسب القواعد السريرية هي: "
                    + medicines
                    + ". لا يتم عرض الجرعات في هذا النظام. "
                    "يجب مراجعة الخطة واعتمادها من الطبيب."
                )
            else:
                message = (
                    "The treatment engine recommends: "
                    + medicines
                    + ". Medication doses are not provided by this system. "
                    "The plan requires clinician review and approval."
                )

        elif treatment_plan["status"] == "URGENT":

            if request.language == "ar":
                message = (
                    "توجد علامة تستدعي تقييمًا طبيًا عاجلًا. "
                    "يجب إجراء تقييم سريري عاجل قبل وضع خطة دوائية."
                )
            else:
                message = (
                    "An urgent clinical condition was detected. "
                    "Urgent clinical assessment is required before "
                    "a medication plan is considered."
                )

        else:

            if request.language == "ar":
                message = (
                    "لا توجد حاليًا قاعدة علاجية مكتملة تنطبق "
                    "على البيانات المتاحة. يجب مراجعة الحالة "
                    "سريريًا قبل اختيار العلاج."
                )
            else:
                message = (
                    "The available clinical data does not match "
                    "a complete treatment rule. Clinician review "
                    "is required before selecting treatment."
                )

"""

if old_start in text:
    start = text.index(old_start)

    next_branch = text.find(
        '    elif prediction:',
        start
    )

    if next_branch == -1:
        raise RuntimeError(
            "Could not locate the next assistant branch."
        )

    text = text[:start] + new_block + text[next_branch:]

# -------------------------------------------------------------------
# 5. Return treatment_plan in API response
# -------------------------------------------------------------------
old = """        context_used=context,
        status="READY",
    )"""

new = """        context_used=context,
        status="READY",
        treatment_plan=treatment_plan,
    )"""

if "treatment_plan=treatment_plan" not in text:
    if old not in text:
        raise RuntimeError("Response return block was not found.")
    text = text.replace(old, new, 1)

# -------------------------------------------------------------------
# 6. Save
# -------------------------------------------------------------------
SOURCE.write_text(text, encoding="utf-8")

print()
print("PATCH COMPLETED SUCCESSFULLY")
print("assistant_api.py updated.")
print("Backup preserved.")
print("=" * 70)