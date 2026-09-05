from pathlib import Path
import shutil

SOURCE = Path("assistant_api.py")
BACKUP = Path("assistant_api_backup_before_arabic_treatment.py")

print("=" * 70)
print("PneumoCare AI — Arabic Treatment Response Patch")
print("=" * 70)

shutil.copy2(SOURCE, BACKUP)

text = SOURCE.read_text(encoding="utf-8")

old = '''            message = (
                f"نتيجة CAPGuard الحالية هي: {prediction}. "
                f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "
                "يمكنني شرح النتيجة والأدلة المستخدمة، لكن القرار الطبي النهائي يجب أن يتم بواسطة طبيب."
            )
'''

new = '''            if treatment_plan["status"] == "RECOMMENDED":

                medicines = "، ".join(
                    treatment_plan["antimicrobial_options"]
                )

                supportive = "، ".join(
                    treatment_plan["supportive_care"]
                )

                monitoring = "، ".join(
                    treatment_plan["monitoring"]
                )

                message = (
                    f"نتيجة CAPGuard الحالية هي: {prediction}. "
                    f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "
                    f"خطة العلاج المقترحة: {medicines}. "
                    f"الرعاية الداعمة: {supportive}. "
                    f"المتابعة المطلوبة: {monitoring}. "
                    "لا يتم عرض جرعات الأدوية بواسطة هذا النظام. "
                    "يجب مراجعة خطة العلاج واعتمادها بواسطة طبيب مختص."
                )

            elif treatment_plan["status"] == "URGENT":

                message = (
                    f"نتيجة CAPGuard الحالية هي: {prediction}. "
                    f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "
                    "تم اكتشاف حالة تستدعي تقييماً سريرياً عاجلاً. "
                    "يجب إجراء تقييم طبي عاجل. "
                    "لا توجد توصية دوائية روتينية لهذه الحالة."
                )

            elif treatment_plan["status"] == "CLINICIAN_REVIEW":

                message = (
                    f"نتيجة CAPGuard الحالية هي: {prediction}. "
                    f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "
                    "لا تدعم الأدلة المتاحة تقديم توصية تلقائية بمضاد حيوي "
                    "لهذه الفئة العمرية. "
                    "يجب مراجعة الحالة بواسطة طبيب مختص."
                )

            else:

                message = (
                    f"نتيجة CAPGuard الحالية هي: {prediction}. "
                    f"احتمال الالتهاب الرئوي في التقييم الحالي هو {probability}. "
                    "المعلومات السريرية المتاحة لا تطابق قاعدة علاج مكتملة. "
                    "يجب مراجعة الحالة بواسطة طبيب مختص."
                )
'''

if old not in text:
    raise RuntimeError(
        "Expected Arabic response block was not found."
    )

text = text.replace(old, new, 1)

SOURCE.write_text(text, encoding="utf-8")

print("PATCH COMPLETED SUCCESSFULLY")
print(f"Backup: {BACKUP}")