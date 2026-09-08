"""
PneumoCare AI
Treatment Rules V1

Clinical decision-support rules.
Based on the WHO 2024 guideline framework for
management of pneumonia in children up to 10 years.

IMPORTANT:
- No medication doses are generated.
- No prescription is generated.
- Rules are intentionally conservative.
- Unsupported/ambiguous cases return CLINICIAN_REVIEW.
"""

WHO_SOURCE = (
    "WHO Guideline on management of pneumonia and diarrhoea "
    "in children up to 10 years of age (2024)"
)

RULE_VERSION = "WHO_2024_TREATMENT_RULES_V1"


TREATMENT_RULES = {

    "2_59_MONTHS_FAST_BREATHING": {
        "age_group": "2-59 months",
        "clinical_category": "pneumonia_fast_breathing",
        "requires_danger_signs": False,
        "antimicrobial_options": [
            "Amoxicillin"
        ],
        "supportive_care": [
            "Clinical hydration assessment",
            "Fever and pain supportive management",
            "Respiratory monitoring"
        ],
        "monitoring": [
            "SpO2",
            "Respiratory rate",
            "Temperature",
            "Heart rate",
            "Clinical response"
        ],
        "disposition": "Outpatient clinical management when no danger signs are present",
        "evidence_source": WHO_SOURCE,
    },

    "2_59_MONTHS_CHEST_INDRAWING": {
        "age_group": "2-59 months",
        "clinical_category": "pneumonia_chest_indrawing",
        "requires_danger_signs": False,
        "antimicrobial_options": [
            "Amoxicillin"
        ],
        "supportive_care": [
            "Clinical hydration assessment",
            "Fever and pain supportive management",
            "Respiratory monitoring"
        ],
        "monitoring": [
            "SpO2",
            "Respiratory rate",
            "Temperature",
            "Heart rate",
            "Chest indrawing",
            "Clinical response"
        ],
        "disposition": "Clinical assessment and appropriate outpatient management when no danger signs are present",
        "evidence_source": WHO_SOURCE,
    },

    "DANGER_SIGNS": {
        "age_group": "Any applicable pediatric age",
        "clinical_category": "general_danger_sign",
        "antimicrobial_options": [],
        "supportive_care": [],
        "monitoring": [
            "SpO2",
            "Respiratory status",
            "Level of consciousness",
            "Hydration status",
            "Clinical deterioration"
        ],
        "disposition": "URGENT_CLINICAL_ASSESSMENT",
        "requires_clinician": True,
        "evidence_source": WHO_SOURCE,
    },

    "HYPOXAEMIA": {
        "age_group": "Pediatric",
        "clinical_category": "hypoxaemia",
        "antimicrobial_options": [],
        "supportive_care": [
            "Urgent oxygenation assessment"
        ],
        "monitoring": [
            "SpO2",
            "Respiratory status",
            "Clinical response"
        ],
        "disposition": "URGENT_CLINICAL_ASSESSMENT",
        "requires_clinician": True,
        "evidence_source": WHO_SOURCE,
    },

    "AGE_5_9_YEARS": {
        "age_group": "5-9 years",
        "clinical_category": "suspected_pneumonia",
        "antimicrobial_options": [],
        "supportive_care": [],
        "monitoring": [
            "SpO2",
            "Respiratory rate",
            "Temperature",
            "Heart rate",
            "Clinical response"
        ],
        "disposition": "CLINICIAN_REVIEW",
        "requires_clinician": True,
        "reason": (
            "WHO 2024 identifies insufficient evidence to recommend "
            "which antibiotic is most effective for children aged 5-9 years."
        ),
        "evidence_source": WHO_SOURCE,
    },
}


def get_rule(rule_name: str):
    """Return a treatment rule by name."""
    return TREATMENT_RULES.get(rule_name)