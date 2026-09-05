from pathlib import Path
import shutil

SOURCE = Path("assistant_api.py")
BACKUP = Path("assistant_api_backup_before_message_patch.py")

print("=" * 70)
print("PneumoCare AI — Assistant Treatment Message Patch")
print("=" * 70)

if not SOURCE.exists():
    raise FileNotFoundError("assistant_api.py was not found.")

shutil.copy2(SOURCE, BACKUP)
print(f"Backup created: {BACKUP}")

text = SOURCE.read_text(encoding="utf-8")

old = '''    elif prediction:

        if pneumonia_probability is not None:
            probability = (
                f"{float(pneumonia_probability) * 100:.1f}%"
            )
        else:
            probability = "available"

        if request.language == "ar":
            message = (
                f"Ù†ØªÙŠØ¬Ø© CAPGuard Ø§Ù„Ø­Ø§Ù„ÙŠØ© Ù‡ÙŠ: {prediction}. "
                f"Ø§Ø­Ø­ØªÙ…Ø§Ù„ Ø§Ù„Ø§Ù„ØªÙ‡Ø§Ø¨ Ø§Ù„Ø±Ø¦ÙˆÙŠ ÙÙŠ Ø§Ù„ØªÙ‚ÙŠÙŠÙ… Ø§Ù„Ø­Ø§Ù„ÙŠ Ù‡Ùˆ "
                f"{probability}. ÙŠÙ…ÙƒÙ†Ù†ÙŠ Ø´Ø±Ø­ Ø§Ù„Ù†ØªÙŠØ¬Ø© ÙˆØ§Ù„Ø£Ø¯Ù„Ø© "
                "Ø§Ù„Ù…Ø³ØªØ®Ø¯Ù…Ø©ØŒ Ù„ÙƒÙ† Ø§Ù„Ù‚Ø±Ø§Ø± Ø§Ù„Ø·Ø¨ÙŠ Ø§Ù„Ù†Ù‡Ø§Ø¦ÙŠ ÙŠØ¬Ø¨ Ø£Ù† "
                "ÙŠØªÙ… Ø¨ÙˆØ§Ø³Ø·Ø© Ø·Ø¨ÙŠØ¨."
            )
        else:
            message = (
                f"The current CAPGuard result is: {prediction}. "
                f"The current pneumonia risk is {probability}. "
                "I can explain the assessment and the evidence "
                "behind it, but the final medical decision must "
                "be made by a qualified clinician."
            )
'''

# The Arabic source text can vary because of terminal encoding.
# Therefore use the exact English branch as the reliable replacement point.
english_old = '''        else:
            message = (
                f"The current CAPGuard result is: {prediction}. "
                f"The current pneumonia risk is {probability}. "
                "I can explain the assessment and the evidence "
                "behind it, but the final medical decision must "
                "be made by a qualified clinician."
            )
'''

english_new = '''        else:
            if treatment_plan["status"] == "RECOMMENDED":
                medicines = ", ".join(
                    treatment_plan["antimicrobial_options"]
                )

                supportive = ", ".join(
                    treatment_plan["supportive_care"]
                )

                monitoring = ", ".join(
                    treatment_plan["monitoring"]
                )

                message = (
                    f"The current CAPGuard result is: {prediction}. "
                    f"The current pneumonia risk is {probability}. "
                    f"Treatment recommendation: {medicines}. "
                    f"Supportive care: {supportive}. "
                    f"Monitoring: {monitoring}. "
                    "Medication doses are not provided by this system. "
                    "The treatment plan requires clinician review and approval."
                )

            elif treatment_plan["status"] == "URGENT":
                message = (
                    f"The current CAPGuard result is: {prediction}. "
                    f"The current pneumonia risk is {probability}. "
                    "An urgent clinical condition was detected. "
                    "Urgent clinical assessment is required. "
                    "No routine antimicrobial recommendation is provided "
                    "for this urgent condition."
                )

            elif treatment_plan["status"] == "CLINICIAN_REVIEW":
                message = (
                    f"The current CAPGuard result is: {prediction}. "
                    f"The current pneumonia risk is {probability}. "
                    "The available evidence does not support an "
                    "automated antimicrobial recommendation for this "
                    "age group. Clinician review is required."
                )

            else:
                message = (
                    f"The current CAPGuard result is: {prediction}. "
                    f"The current pneumonia risk is {probability}. "
                    "No complete treatment rule matches the available "
                    "clinical information. Clinician review is required."
                )
'''

if english_old not in text:
    raise RuntimeError(
        "The expected English prediction response was not found."
    )

text = text.replace(english_old, english_new, 1)

SOURCE.write_text(text, encoding="utf-8")

print()
print("PATCH COMPLETED SUCCESSFULLY")
print("Assistant treatment response updated.")
print(f"Backup: {BACKUP}")
print("=" * 70)