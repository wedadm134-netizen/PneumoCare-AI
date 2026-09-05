from pathlib import Path
import shutil

SOURCE = Path("assistant_api.py")
BACKUP = Path("assistant_api_backup_before_arabic_treatment_v2.py")

print("=" * 70)
print("PneumoCare AI — Arabic Treatment Message V2")
print("=" * 70)

if not SOURCE.exists():
    raise FileNotFoundError("assistant_api.py not found.")

# Backup
shutil.copy2(SOURCE, BACKUP)
print(f"Backup created: {BACKUP}")

# Preserve the existing file encoding exactly as UTF-8
text = SOURCE.read_text(encoding="utf-8")
lines = text.splitlines()

# assistant_api.py lines 239-246 are the old Arabic prediction message.
# Python list indexes are zero-based => 238:246
start = 238
end = 246

if len(lines) < end:
    raise RuntimeError(
        f"assistant_api.py has only {len(lines)} lines; "
        f"expected at least {end}."
    )

# Verify the target area structurally before modifying it.
target = "\n".join(lines[start:end])

if 'if request.language == "ar":' not in target:
    raise RuntimeError(
        "Target Arabic branch was not found in expected lines 239-246."
    )

replacement = [
    '        if request.language == "ar":',
    '',
    '            if treatment_plan["status"] == "RECOMMENDED":',
    '',
    '                medicines = "، ".join(',
    '                    treatment_plan["antimicrobial_options"]',
    '                )',
    '',
    '                supportive = "، ".join(',
    '                    treatment_plan["supportive_care"]',
    '                )',
    '',
    '                monitoring = "، ".join(',
    '                    treatment_plan["monitoring"]',
    '                )',
    '',
    '                message = (',
    '                    f"نتيجة CAPGuard الحالية هي: {prediction}. "',
    '                    f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "',
    '                    f"خطة العلاج المقترحة: {medicines}. "',
    '                    f"الرعاية الداعمة: {supportive}. "',
    '                    f"المتابعة المطلوبة: {monitoring}. "',
    '                    "لا يتم عرض جرعات الأدوية بواسطة هذا النظام. "',
    '                    "يجب مراجعة خطة العلاج واعتمادها بواسطة طبيب مختص."',
    '                )',
    '',
    '            elif treatment_plan["status"] == "URGENT":',
    '',
    '                message = (',
    '                    f"نتيجة CAPGuard الحالية هي: {prediction}. "',
    '                    f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "',
    '                    "تم اكتشاف حالة تستدعي تقييماً سريرياً عاجلاً. "',
    '                    "يجب إجراء تقييم طبي عاجل. "',
    '                    "لا توجد توصية دوائية روتينية لهذه الحالة."',
    '                )',
    '',
    '            elif treatment_plan["status"] == "CLINICIAN_REVIEW":',
    '',
    '                message = (',
    '                    f"نتيجة CAPGuard الحالية هي: {prediction}. "',
    '                    f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "',
    '                    "لا تدعم الأدلة المتاحة تقديم توصية تلقائية بمضاد حيوي "',
    '                    "لهذه الفئة العمرية. "',
    '                    "يجب مراجعة الحالة بواسطة طبيب مختص."',
    '                )',
    '',
    '            else:',
    '',
    '                message = (',
    '                    f"نتيجة CAPGuard الحالية هي: {prediction}. "',
    '                    f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "',
    '                    "المعلومات السريرية المتاحة لا تطابق قاعدة علاج مكتملة. "',
    '                    "يجب مراجعة الحالة بواسطة طبيب مختص."',
    '                )',
]

# Important:
# Keep the existing `else:` English branch that starts after line 246.
# We replace only the Arabic block.
lines[start:end] = replacement

SOURCE.write_text("\n".join(lines) + "\n", encoding="utf-8")

print()
print("PATCH COMPLETED SUCCESSFULLY")
print("Arabic treatment response has been updated.")
print(f"Backup: {BACKUP}")
print("=" * 70)