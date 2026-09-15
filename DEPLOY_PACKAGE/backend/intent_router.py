def classify_question_intent(question: str) -> str:
    """
    Lightweight first-pass intent classifier.
    Returns:
      casual
      patient_assessment
      xray
      conflict
      treatment
      general_medical
    """

    q = (question or "").strip().lower()

    casual_phrases = [
        "عامل ايه",
        "عامل إيه",
        "اخبارك ايه",
        "أخبارك إيه",
        "ازيك",
        "إزيك",
        "الدنيا معاك ايه",
        "الدنيا معاك إيه",
        "how are you",
        "how's it going",
        "what's up",
    ]

    if any(phrase in q for phrase in casual_phrases):
        return "casual"

    xray_phrases = [
        "الأشعة",
        "اشعة",
        "x-ray",
        "xray",
        "radiograph",
    ]

    if any(phrase in q for phrase in xray_phrases):
        return "xray"

    conflict_phrases = [
        "تعارض",
        "متفقة",
        "مش متفقة",
        "الاختلاف",
        "سبب التعارض",
        "ليه النتيجة",
        "why do the results differ",
        "conflict",
    ]

    if any(phrase in q for phrase in conflict_phrases):
        return "conflict"

    treatment_phrases = [
        "العلاج",
        "نعالج",
        "خطة العلاج",
        "treatment",
        "treat",
        "medication",
        "دواء",
    ]

    if any(phrase in q for phrase in treatment_phrases):
        return "treatment"

    patient_phrases = [
        "حالة المريض",
        "حالة المريضة",
        "الحالة",
        "تقييم الحالة",
        "النتيجة النهائية",
        "طمّني على المريضة",
        "طمني على المريضة",
        "طمّني على المريض",
        "طمني على المريض",
        "patient",
        "assessment",
    ]

    if any(phrase in q for phrase in patient_phrases):
        return "patient_assessment"

    return "general_medical"


if __name__ == "__main__":
    tests = [
        "عامل ايه؟",
        "طمني على المريضة",
        "الأشعة بتقول إيه؟",
        "ليه النتيجة مش متفقة؟",
        "إيه العلاج؟",
        "ما هي أعراض الالتهاب الرئوي؟",
    ]

    for text in tests:
        print(f"{text} -> {classify_question_intent(text)}")

def detect_question_language(question: str) -> str:
    q = question or ""
    arabic_chars = sum(1 for ch in q if 0x600 <= ord(ch) <= 0x6FF)
    return "ar" if arabic_chars >= 2 else "en"
