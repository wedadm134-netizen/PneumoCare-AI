import { useEffect, useState } from "react";
import "./App.css";

const API_BASE_URL = "";

const translations = {
  en: {
    brand: "PneumoCare AI",
    tagline: "Intelligent Pneumonia Assessment",
    fullTagline:
      "Intelligent Pneumonia Assessment & Clinical Decision Support",
    home: "Home",
    features: "Features",
    about: "About",
    start: "Start Assessment",
    explore: "Explore System",
    aiSupport: "AI-Powered Clinical Decision Support",
    heroTitle1: "Smarter Pneumonia",
    heroTitle2: "Assessment with AI",
    heroText:
      "PneumoCare AI brings together clinical information, vital signs, and chest X-ray analysis to support pneumonia assessment.",
    imaging: "Imaging",
    imagingText: "Chest X-ray analysis",
    clinical: "Clinical Information",
    clinicalText: "Clinical notes analysis",
    vital: "Vital Signs",
    vitalText: "Structured clinical evidence",
    production: "PRODUCTION",
    engineReady: "System Ready",
    hybrid: "AI EVIDENCE",
    featuresTitle: "Multiple Sources. One Intelligent Assessment.",
    featuresText:
      "PneumoCare AI combines complementary clinical evidence to support a more informed assessment.",
    xrayFeature: "Chest X-Ray Analysis",
    xrayFeatureText:
      "AI-assisted chest X-ray analysis for Normal and Pneumonia classification.",
    nlpFeature: "Clinical Information Analysis",
    nlpFeatureText:
      "Clinical notes are analyzed for pneumonia-related evidence.",
    vitalFeature: "Vital Signs Analysis",
    vitalFeatureText:
      "Vital signs are analyzed as structured clinical evidence.",
    safetyShort:
      "Clinical decision support only. Results require qualified clinical review and confirmation.",
    release: "Production Release V1",

    patientManagement: "Patient Management",
    newAssessment: "Start a New Assessment",
    patientSelectionText:
      "Create a patient case or continue with an existing patient record.",
    newPatient: "NEW PATIENT",
    createPatient: "Create New Patient",
    createPatientText:
      "Create a patient profile and begin a new assessment.",
    continue: "Continue",
    existingPatient: "EXISTING PATIENT",
    openExisting: "Open Existing Patient",
    existingText:
      "Search patient records and review previous assessments and clinical history.",
    searchPatient: "Search Patient",
    privacyNote:
      "Patient information is handled within the PneumoCare AI system.",

    back: "Back",
    newPatientBadge: "New Patient",
    createCase: "Create Patient Case",
    basicInfo:
      "Enter the patient's basic information to create a patient record.",
    patientName: "Patient Name",
    enterPatientName: "Enter patient name",
    age: "Age",
    enterAge: "Enter age",
    sex: "Biological Sex",
    selectSex: "Select Biological Sex",
    male: "Male",
    female: "Female",
    creating: "Creating Patient...",
    createCaseButton: "Create Patient Case",

    history: "Clinical History",
    historyBadge: "Patient History",
    historyTitle: "Patient Clinical History",
    historyIntro:
      "Search for an existing patient to review previous visits and assessments.",
    patientId: "Patient ID",
    patientIdPlaceholder: "Enter patient ID",
    patientIdRequired: "Please enter a Patient ID.",
    lastPatientId: "Last used Patient ID",
    useLastId: "Use this ID",
    loadHistory: "View Clinical History",
    loadingHistory: "Loading History...",
    historyError:
      "Unable to load the patient's clinical history.",
    noHistory:
      "No previous clinical visits were found for this patient.",
    visits: "Visits",
    visit: "Visit",
    visitDate: "Visit Date",
    assessment: "Assessment",
    risk: "Pneumonia Risk",
    severity: "Severity",
    clinicalNotes: "Clinical Notes",
    vitals: "Vital Signs",
    cbc: "Laboratory Results — CBC",
    xray: "Chest X-Ray",
    noData: "Not available",
    newVisit: "Start New Visit",
    patientProfile: "Patient Profile",
    viewHistory: "View History",

    assessmentBadge: "Clinical Assessment",
    assessmentTitle: "Pneumonia Assessment",
    assessmentText:
      "Provide the available clinical information and chest X-ray to run the AI assessment.",
    clinicalInfo: "Clinical Information",
    clinicalInfoDesc:
      "Enter available clinical findings and vital signs.",
    temperature: "Temperature (°C)",
    heartRate: "Heart Rate (bpm)",
    oxygen: "Oxygen Saturation (%)",
    required: "required",
    notesPlaceholder:
      "Enter symptoms, clinical findings, examination notes, respiratory signs, duration of fever, cough, and other relevant observations.",
    cbcDesc: "Optional laboratory information.",
    wbc: "WBC",
    neutrophils: "Neutrophils (%)",
    lymphocytes: "Lymphocytes (%)",
    hemoglobin: "Hemoglobin",
    platelets: "Platelets",
    cbcNote:
      "CBC values are optional clinical information and may be stored with the assessment.",
    chestXray: "Chest X-Ray",
    xrayDesc: "Upload a PNG, JPG, JPEG, or WEBP chest X-ray.",
    upload: "Upload Chest X-Ray",
    formats: "PNG, JPG, JPEG or WEBP",
    selected: "X-ray selected successfully",
    cancel: "Cancel",
    runAssessment: "Run PneumoCare AI",
    running: "Running AI Assessment...",
    assessmentError: "Assessment Error",
    complete: "AI Assessment Complete",

    resultTitle: "PneumoCare AI Assessment Result",
    resultText:
      "Integrated assessment based on the available clinical information, vital signs, and chest X-ray evidence.",
    overall: "OVERALL FUSION ASSESSMENT",

    normal: "Normal",
    pneumonia: "Pneumonia",

    overallRiskContext:
      "Based on Clinical Notes + Laboratory Findings",

    normalLikelihood: "Normal Likelihood",
    riskLevel: "Clinical Risk Level",
    low: "Low",
    moderate: "Moderate",
    high: "High",

    evidence: "AI EVIDENCE",
    evidenceTitle: "Available Evidence",
    analyzed: "Analyzed",
    unavailable: "Unavailable",
    clinicalEvidence: "Clinical Information",
    vitalEvidence: "Vital Signs",
    xrayEvidence: "Chest X-Ray",
    xraySeparate:
      "Each source is shown separately so the clinical assessment and chest X-ray assessment remain clear and independently interpretable.",
    clinicalFinal: "FINAL CLINICAL ASSESSMENT",
    clinicalSources: "Clinical Notes + Vital Signs + Laboratory Results",
    xrayFinal: "FINAL X-RAY ASSESSMENT",
    xraySource: "Chest X-Ray AI Analysis",
    pneumoniaProbability: "Pneumonia Probability",
    normalProbability: "Normal Probability",
    sourceEstimateNote: "Model estimate from this evidence source",

    reasoning: "AI REASONING & EVIDENCE",
    reasoningTitle: "Why this assessment?",
    reasoningText:
      "The overall assessment considers the available clinical information and vital signs, while the chest X-ray provides additional independent imaging evidence.",
    conflictTitle: "Important Evidence Difference",
    conflictText:
      "The chest X-ray result differs from the overall clinical assessment. This difference should be reviewed together with the patient's complete clinical picture.",

    imagingExplanation: "EXPLAINABLE IMAGING",
    imagingTitle: "Chest X-Ray AI Explanation",
    imagingText:
      "The attention map highlights image regions that influenced the X-ray model prediction. It is an explainability aid and is not proof of disease.",
    originalXray: "ORIGINAL CHEST X-RAY",
    attentionMap: "AI ATTENTION MAP",
    imageUnavailable:
      "Original image is stored with the patient assessment.",
    gradUnavailable:
      "AI attention map is unavailable for this assessment.",
    prediction: "AI Assessment",
    likelihood: "Pneumonia Likelihood",
    interpretation: "How to interpret this image",

    severitySection: "CLINICAL ASSESSMENT",
    severityTitle: "Severity Assessment",
    severityLevel: "Severity Level",
    signals: "Clinical Signals",
    noHighRisk: "No high-risk clinical signals identified.",

    considerations: "CLINICAL CONSIDERATIONS",
    considerationsTitle: "What should be considered?",

    safetyTitle: "CLINICAL DECISION SUPPORT ONLY",
    safetyText:
      "PneumoCare AI is an assistive medical AI system. Results require qualified clinician review and confirmation. The system does not provide autonomous prescriptions, antibiotic dosing, or independent treatment decisions.",

    unknown: "Unknown",
    noPatient: "No patient case is selected.",
    notesRequired: "Clinical notes are required for the assessment.",
    xrayRequired:
      "Please upload a chest X-ray before running the assessment.",
    backendError:
      "Unable to connect to the PneumoCare AI backend.",
    assessmentBackendError:
      "Unable to connect to the AI assessment engine.",

    treatment: "CLINICAL MANAGEMENT",
    treatmentTitle: "Treatment Plan",
    treatmentIntro:
      "A structured treatment recommendation based on the current clinical assessment.",
    medication: "Medication",
    medications: "Medications",
    noMedication: "No routine medication recommendation.",
    supportiveCare: "Supportive Care",
    monitoring: "Monitoring",
    clinicalStatus: "Clinical Status",
    redFlags: "Red Flags",
    clinicianReview: "Clinician Review",
    recommended: "Recommended",
    urgent: "Urgent Clinical Review",
    clinicianReviewStatus: "Clinician Review Required",
    treatmentUnavailable:
      "A treatment plan is not available for this assessment.",
    noSupportiveCare:
      "No additional supportive-care recommendation is available.",
    noMonitoring:
      "No specific monitoring recommendation is available.",
    noRedFlags: "No additional red flags were identified.",
    medicationSafety:
      "Medication doses are not displayed by this system.",
    treatmentDisclaimer:
      "This treatment plan is decision support and requires clinician review and approval.",
    evidenceSource: "Evidence source",
    whoGuideline:
      "WHO guideline for management of pneumonia and diarrhoea in children",

    assistant: "AI ASSISTANT",
    assistantTitle: "Ask PneumoCare AI",
    assistantIntro:
      "Ask questions about this assessment and receive an AI-generated explanation based on the available clinical evidence.",
    assistantPlaceholder:
      "Ask about this assessment...",
    assistantSend: "Ask AI",
    assistantThinking:
      "PneumoCare AI is thinking...",
    assistantWelcome:
      "I can explain the assessment, evidence differences, X-ray findings, risk level, and clinical considerations.",
    assistantYou: "You",
    assistantAI: "PneumoCare AI",
    assistantError:
      "Unable to get a response from the AI assistant.",
    assistantEmpty:
      "Ask a question about the current patient assessment.",
  },

  ar: {
    brand: "PneumoCare AI",
    tagline: "التقييم الذكي للالتهاب الرئوي",
    fullTagline:
      "التقييم الذكي للالتهاب الرئوي ودعم القرار السريري",
    home: "الرئيسية",
    features: "المميزات",
    about: "عن النظام",
    start: "بدء التقييم",
    explore: "استكشاف النظام",
    aiSupport: "دعم القرار السريري بالذكاء الاصطناعي",
    heroTitle1: "تقييم أذكى للالتهاب الرئوي",
    heroTitle2: "باستخدام الذكاء الاصطناعي",
    heroText:
      "يجمع PneumoCare AI المعلومات السريرية والعلامات الحيوية وتحليل أشعة الصدر لدعم تقييم الالتهاب الرئوي.",
    imaging: "الأشعة",
    imagingText: "تحليل أشعة الصدر",
    clinical: "المعلومات السريرية",
    clinicalText: "تحليل الملاحظات السريرية",
    vital: "العلامات الحيوية",
    vitalText: "الأدلة السريرية المنظمة",
    production: "إصدار إنتاجي",
    engineReady: "النظام جاهز",
    hybrid: "الأدلة المدعومة بالذكاء الاصطناعي",
    featuresTitle: "مصادر متعددة. تقييم ذكي واحد.",
    featuresText:
      "يجمع PneumoCare AI الأدلة السريرية المختلفة لدعم تقييم أكثر شمولًا.",
    xrayFeature: "تحليل أشعة الصدر",
    xrayFeatureText:
      "تحليل مدعوم بالذكاء الاصطناعي لأشعة الصدر لتصنيف الحالة.",
    nlpFeature: "تحليل المعلومات السريرية",
    nlpFeatureText:
      "تحليل الملاحظات السريرية لاستخراج الأدلة المرتبطة بالالتهاب الرئوي.",
    vitalFeature: "تحليل العلامات الحيوية",
    vitalFeatureText:
      "تحليل العلامات الحيوية كأدلة سريرية منظمة.",
    safetyShort:
      "للدعم السريري فقط. يجب مراجعة النتائج وتأكيدها بواسطة مختص مؤهل.",
    release: "الإصدار الإنتاجي الأول",

    patientManagement: "إدارة المرضى",
    newAssessment: "بدء تقييم جديد",
    patientSelectionText:
      "أنشئ حالة مريض جديدة أو تابع باستخدام سجل موجود.",
    newPatient: "مريض جديد",
    createPatient: "إنشاء مريض جديد",
    createPatientText:
      "أنشئ ملف المريض وابدأ تقييمًا جديدًا.",
    continue: "متابعة",
    existingPatient: "مريض موجود",
    openExisting: "فتح مريض موجود",
    existingText:
      "ابحث في سجلات المرضى وراجع التقييمات والتاريخ السريري.",
    searchPatient: "البحث عن مريض",
    privacyNote:
      "يتم التعامل مع معلومات المريض داخل نظام PneumoCare AI.",

    back: "رجوع",
    newPatientBadge: "مريض جديد",
    createCase: "إنشاء حالة مريض",
    basicInfo:
      "أدخل البيانات الأساسية للمريض لإنشاء سجل جديد.",
    patientName: "اسم المريض",
    enterPatientName: "أدخل اسم المريض",
    age: "العمر",
    enterAge: "أدخل العمر",
    sex: "الجنس البيولوجي",
    selectSex: "اختر الجنس البيولوجي",
    male: "ذكر",
    female: "أنثى",
    creating: "جارٍ إنشاء المريض...",
    createCaseButton: "إنشاء حالة المريض",

    history: "التاريخ السريري",
    historyBadge: "سجل المريض",
    historyTitle: "التاريخ السريري للمريض",
    historyIntro:
      "ابحث عن مريض موجود لمراجعة الزيارات والتقييمات السابقة.",
    patientId: "رقم المريض",
    patientIdPlaceholder: "أدخل رقم المريض",
    patientIdRequired: "يرجى إدخال رقم المريض.",
    lastPatientId: "آخر رقم مريض مستخدم",
    useLastId: "استخدم هذا الرقم",
    loadHistory: "عرض التاريخ السريري",
    loadingHistory: "جارٍ تحميل التاريخ...",
    historyError:
      "تعذر تحميل التاريخ السريري للمريض.",
    noHistory:
      "لم يتم العثور على زيارات سريرية سابقة لهذا المريض.",
    visits: "الزيارات",
    visit: "زيارة",
    visitDate: "تاريخ الزيارة",
    assessment: "التقييم",
    risk: "احتمالية الالتهاب الرئوي",
    severity: "الشدة",
    clinicalNotes: "الملاحظات السريرية",
    vitals: "العلامات الحيوية",
    cbc: "نتائج المختبر — CBC",
    xray: "أشعة الصدر",
    noData: "غير متاح",
    newVisit: "بدء زيارة جديدة",
    patientProfile: "بيانات المريض",
    viewHistory: "عرض التاريخ",

    assessmentBadge: "التقييم السريري",
    assessmentTitle: "تقييم الالتهاب الرئوي",
    assessmentText:
      "أدخل المعلومات السريرية المتاحة وأشعة الصدر لإجراء التقييم بالذكاء الاصطناعي.",
    clinicalInfo: "المعلومات السريرية",
    clinicalInfoDesc:
      "أدخل العلامات السريرية والعلامات الحيوية المتاحة.",
    temperature: "درجة الحرارة (°C)",
    heartRate: "معدل ضربات القلب (نبضة/دقيقة)",
    oxygen: "تشبع الأكسجين (%)",
    required: "مطلوب",
    notesPlaceholder:
      "أدخل الأعراض، نتائج الفحص، العلامات التنفسية، مدة الحمى والسعال وأي ملاحظات مهمة أخرى.",
    cbcDesc: "معلومات مخبرية اختيارية.",
    wbc: "كريات الدم البيضاء WBC",
    neutrophils: "العدلات (%)",
    lymphocytes: "الخلايا الليمفاوية (%)",
    hemoglobin: "الهيموجلوبين",
    platelets: "الصفائح الدموية",
    cbcNote:
      "قيم CBC معلومات سريرية اختيارية ويمكن حفظها مع التقييم.",
    chestXray: "أشعة الصدر",
    xrayDesc:
      "ارفع صورة أشعة بصيغة PNG أو JPG أو JPEG أو WEBP.",
    upload: "رفع أشعة الصدر",
    formats: "PNG أو JPG أو JPEG أو WEBP",
    selected: "تم اختيار الأشعة بنجاح",
    cancel: "إلغاء",
    runAssessment: "تشغيل PneumoCare AI",
    running: "جارٍ إجراء التقييم...",
    assessmentError: "خطأ في التقييم",
    complete: "اكتمل التقييم",

    resultTitle: "نتيجة تقييم PneumoCare AI",
    resultText:
      "تقييم متكامل يعتمد على المعلومات السريرية والعلامات الحيوية وأدلة أشعة الصدر المتاحة.",
    overall: "التقييم النهائي المدمج",

    normal: "طبيعي",
    pneumonia: "التهاب رئوي",

    overallRiskContext:
      "بناءً على الملاحظات السريرية ونتائج المختبر",

    normalLikelihood: "احتمالية الحالة الطبيعية",
    riskLevel: "مستوى الخطورة السريري",
    low: "منخفض",
    moderate: "متوسط",
    high: "مرتفع",

    evidence: "أدلة الذكاء الاصطناعي",
    evidenceTitle: "الأدلة المتاحة",
    analyzed: "تم التحليل",
    unavailable: "غير متاح",
    clinicalEvidence: "المعلومات السريرية",
    vitalEvidence: "العلامات الحيوية",
    xrayEvidence: "أشعة الصدر",
    xraySeparate:
      "يتم عرض كل مصدر بشكل مستقل حتى تظل النتيجة السريرية ونتيجة أشعة الصدر واضحتين وقابلتين للتفسير بشكل منفصل.",
    clinicalFinal: "النتيجة النهائية للمعلومات السريرية",
    clinicalSources: "الملاحظات السريرية + العلامات الحيوية + نتائج المختبر",
    xrayFinal: "النتيجة النهائية لأشعة الصدر",
    xraySource: "تحليل أشعة الصدر بالذكاء الاصطناعي",
    pneumoniaProbability: "احتمالية الالتهاب الرئوي",
    normalProbability: "احتمالية الحالة الطبيعية",
    sourceEstimateNote: "تقدير النموذج بناءً على مصدر الأدلة هذا",

    reasoning: "منطق وأدلة الذكاء الاصطناعي",
    reasoningTitle: "لماذا ظهرت هذه النتيجة؟",
    reasoningText:
      "يعتمد التقييم النهائي على المعلومات السريرية والعلامات الحيوية المتاحة، بينما توفر أشعة الصدر دليلًا تصويريًا إضافيًا مستقلًا.",
    conflictTitle: "اختلاف مهم بين الأدلة",
    conflictText:
      "نتيجة أشعة الصدر تختلف عن التقييم السريري النهائي. يجب مراجعة هذا الاختلاف مع الصورة السريرية الكاملة للمريض.",

    imagingExplanation: "التفسير التصويري",
    imagingTitle: "تفسير الذكاء الاصطناعي لأشعة الصدر",
    imagingText:
      "توضح خريطة الانتباه مناطق الصورة التي أثرت في توقع نموذج الأشعة. وهي أداة للتفسير وليست دليلًا مؤكدًا على وجود المرض.",
    originalXray: "أشعة الصدر الأصلية",
    attentionMap: "خريطة انتباه الذكاء الاصطناعي",
    imageUnavailable:
      "تم حفظ الصورة الأصلية مع تقييم المريض.",
    gradUnavailable:
      "خريطة الانتباه غير متاحة لهذا التقييم.",
    prediction: "تقييم الذكاء الاصطناعي",
    likelihood: "احتمالية الالتهاب الرئوي",
    interpretation: "كيفية قراءة الصورة",

    severitySection: "التقييم السريري",
    severityTitle: "تقييم شدة الحالة",
    severityLevel: "مستوى الشدة",
    signals: "المؤشرات السريرية",
    noHighRisk:
      "لم يتم تحديد مؤشرات سريرية عالية الخطورة.",

    considerations: "اعتبارات سريرية",
    considerationsTitle: "ما الذي ينبغي مراعاته؟",

    safetyTitle: "للدعم السريري فقط",
    safetyText:
      "PneumoCare AI نظام مساعد للذكاء الاصطناعي الطبي. يجب مراجعة النتائج وتأكيدها بواسطة طبيب أو مختص مؤهل. لا يقدم النظام وصفات دوائية مستقلة أو جرعات للمضادات الحيوية أو قرارات علاجية ذاتية.",

    unknown: "غير معروف",
    noPatient: "لم يتم اختيار حالة مريض.",
    notesRequired:
      "الملاحظات السريرية مطلوبة لإجراء التقييم.",
    xrayRequired:
      "يرجى رفع أشعة الصدر قبل إجراء التقييم.",
    backendError:
      "تعذر الاتصال بخادم PneumoCare AI.",
    assessmentBackendError:
      "تعذر الاتصال بمحرك التقييم بالذكاء الاصطناعي.",

    treatment: "الإدارة العلاجية",
    treatmentTitle: "خطة العلاج",
    treatmentIntro:
      "خطة علاجية منظمة مبنية على التقييم السريري الحالي.",
    medication: "الدواء",
    medications: "الأدوية",
    noMedication:
      "لا توجد توصية دوائية روتينية حاليًا.",
    supportiveCare: "الرعاية الداعمة",
    monitoring: "المتابعة والمراقبة",
    clinicalStatus: "الحالة السريرية",
    redFlags: "علامات تستدعي الانتباه",
    clinicianReview: "مراجعة الطبيب",
    recommended: "موصى به",
    urgent: "مراجعة سريرية عاجلة",
    clinicianReviewStatus: "تتطلب مراجعة الطبيب",
    treatmentUnavailable:
      "لا توجد خطة علاجية متاحة لهذا التقييم.",
    noSupportiveCare:
      "لا توجد توصية إضافية للرعاية الداعمة.",
    noMonitoring:
      "لا توجد توصية محددة للمراقبة.",
    noRedFlags:
      "لم يتم تحديد علامات خطر إضافية.",
    medicationSafety:
      "لا يتم عرض جرعات الأدوية بواسطة هذا النظام.",
    treatmentDisclaimer:
      "هذه الخطة أداة لدعم القرار السريري وتتطلب مراجعة واعتماد الطبيب.",
    evidenceSource: "المصدر العلمي",
    whoGuideline:
      "إرشادات منظمة الصحة العالمية لإدارة الالتهاب الرئوي والإسهال لدى الأطفال",

    assistant: "مساعد الذكاء الاصطناعي",
    assistantTitle: "اسأل PneumoCare AI",
    assistantIntro:
      "يمكنك طرح أسئلة حول هذا التقييم والحصول على شرح مولد بالذكاء الاصطناعي بناءً على الأدلة السريرية المتاحة.",
    assistantPlaceholder:
      "اسأل عن نتيجة هذا التقييم...",
    assistantSend: "اسأل الذكاء الاصطناعي",
    assistantThinking:
      "PneumoCare AI يفكر...",
    assistantWelcome:
      "يمكنني شرح نتيجة التقييم، اختلاف الأدلة، نتيجة الأشعة، مستوى الخطورة، والاعتبارات السريرية.",
    assistantYou: "أنت",
    assistantAI: "PneumoCare AI",
    assistantError:
      "تعذر الحصول على رد من مساعد الذكاء الاصطناعي.",
    assistantEmpty:
      "اطرح سؤالًا عن تقييم المريض الحالي.",
  },
};

function App() {
  const [lang, setLang] = useState("en");
  const t = translations[lang];

  const [screen, setScreen] = useState("home");

  const [patientName, setPatientName] = useState("");
  const [patientAge, setPatientAge] = useState("");
  const [biologicalSex, setBiologicalSex] = useState("");
  const [createdPatient, setCreatedPatient] = useState(null);
  const [creatingPatient, setCreatingPatient] = useState(false);
  const [patientError, setPatientError] = useState("");

  // ============================================================
  // HISTORY STATE
  // ============================================================

  const [historyPatientId, setHistoryPatientId] =
    useState(() => {
      try {
        return localStorage.getItem("pneumocare_last_patient_id") || "";
      } catch {
        return "";
      }
    });

  const [patientHistory, setPatientHistory] =
    useState(null);

  const [loadingHistory, setLoadingHistory] =
    useState(false);

  const [historyError, setHistoryError] =
    useState("");

  // ============================================================
  // ASSESSMENT STATE
  // ============================================================

  const [clinicalNote, setClinicalNote] =
    useState("");

  const [temperature, setTemperature] =
    useState("");

  const [heartRate, setHeartRate] =
    useState("");

  const [oxygenSaturation, setOxygenSaturation] =
    useState("");

  const [cbcData, setCbcData] = useState({
    wbc: "",
    neutrophils: "",
    lymphocytes: "",
    hemoglobin: "",
    platelets: "",
  });

  const [xrayFile, setXrayFile] =
    useState(null);

  const [xrayPreviewUrl, setXrayPreviewUrl] =
    useState(null);

  const [runningAssessment, setRunningAssessment] =
    useState(false);

  const [assessmentError, setAssessmentError] =
    useState("");

  const [assessmentResult, setAssessmentResult] =
    useState(null);

  const [treatmentPlan, setTreatmentPlan] =
    useState(null);

  // ============================================================
  // ASSISTANT STATE
  // ============================================================

  const [assistantMessages, setAssistantMessages] =
    useState([]);

  const [assistantInput, setAssistantInput] =
    useState("");

  const [assistantLoading, setAssistantLoading] =
    useState(false);

  const [assistantError, setAssistantError] =
    useState("");

  useEffect(() => {
    document.documentElement.lang = lang;
    document.documentElement.dir =
      lang === "ar" ? "rtl" : "ltr";
  }, [lang]);

  useEffect(() => {
    return () => {
      if (xrayPreviewUrl) {
        URL.revokeObjectURL(xrayPreviewUrl);
      }
    };
  }, [xrayPreviewUrl]);

  useEffect(() => {
    try {
      if (historyPatientId) {
        localStorage.setItem(
          "pneumocare_last_patient_id",
          historyPatientId
        );
      }
    } catch {
      // ignore storage errors
    }
  }, [historyPatientId]);

  // Keep History input in sync with the active patient
  useEffect(() => {
    const id = createdPatient?.patient_id;
    if (id) {
      setHistoryPatientId((prev) => {
        if (prev && String(prev).trim()) {
          return prev;
        }
        return String(id);
      });
    }
  }, [createdPatient]);

  const switchLanguage = (nextLang) => {
    setLang(nextLang);
  };

  const openAssessment = () => {
    setScreen("patient-selection");
  };

  const goHome = () => {
    setScreen("home");
    setPatientError("");
    setAssessmentError("");
    setHistoryError("");
  };

  const openNewPatient = () => {
    setPatientError("");
    setPatientName("");
    setPatientAge("");
    setBiologicalSex("");
    setScreen("new-patient");
  };

  const openExistingPatient = () => {
    // Prefer current state → created patient → localStorage
    setHistoryPatientId((prev) => {
      if (prev && String(prev).trim()) {
        return String(prev).trim();
      }
      if (createdPatient?.patient_id) {
        return String(createdPatient.patient_id);
      }
      try {
        const stored = localStorage.getItem(
          "pneumocare_last_patient_id"
        );
        if (stored && stored.trim()) {
          return stored.trim();
        }
      } catch {
        // ignore
      }
      return prev || "";
    });
    setScreen("existing-patient");
    setPatientHistory(null);
    setHistoryError("");
  };

  const backToPatientSelection = () => {
    setScreen("patient-selection");
    setPatientError("");
    setHistoryError("");
  };

  // ============================================================
  // CREATE NEW PATIENT
  // ============================================================

  const createPatient = async (event) => {
    event.preventDefault();

    setPatientError("");
    setCreatingPatient(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/patients`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            patient_name: patientName.trim(),
            age: Number(patientAge),
            biological_sex: biologicalSex,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail
            ? typeof data.detail === "string"
              ? data.detail
              : JSON.stringify(data.detail)
            : t.backendError
        );
      }

      const patient = data.patient || data;

      if (!patient?.patient_id) {
        throw new Error(t.backendError);
      }

      setCreatedPatient(patient);
      setHistoryPatientId(String(patient.patient_id));

      try {
        localStorage.setItem(
          "pneumocare_last_patient_id",
          String(patient.patient_id)
        );
      } catch {
        // ignore
      }

      setClinicalNote("");
      setTemperature("");
      setHeartRate("");
      setOxygenSaturation("");

      setCbcData({
        wbc: "",
        neutrophils: "",
        lymphocytes: "",
        hemoglobin: "",
        platelets: "",
      });

      if (xrayPreviewUrl) {
        URL.revokeObjectURL(xrayPreviewUrl);
      }

      setXrayFile(null);
      setXrayPreviewUrl(null);

      setAssessmentResult(null);
      setTreatmentPlan(null);
      setAssessmentError("");

      setAssistantMessages([]);
      setAssistantInput("");
      setAssistantError("");
      setAssistantLoading(false);

      setScreen("assessment");
    } catch (error) {
      console.error(
        "Patient creation error:",
        error
      );

      setPatientError(
        error.message || t.backendError
      );
    } finally {
      setCreatingPatient(false);
    }
  };

  // ============================================================
  // HISTORY
  // ============================================================

  const loadPatientHistory = async (event) => {
    if (event) {
      event.preventDefault();
    }

    const patientId =
      historyPatientId.trim();

    setHistoryError("");

    if (!patientId) {
      setHistoryError(
        t.patientIdRequired
      );
      return;
    }

    setLoadingHistory(true);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/history/${encodeURIComponent(
          patientId
        )}`
      );

      let data = null;

      try {
        data = await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        const detail =
          data?.detail ||
          data?.error ||
          data?.message ||
          t.historyError;

        throw new Error(
          typeof detail === "string"
            ? detail
            : JSON.stringify(detail)
        );
      }

      setPatientHistory(data);

      // Always keep the ID the user just queried
      setHistoryPatientId(String(patientId));

      const patient =
        normalizeHistoryPatient(
          data,
          patientId
        );

      if (patient) {
        setCreatedPatient(patient);

        setPatientName(
          patient.patient_name || ""
        );

        setPatientAge(
          patient.age !== null &&
            patient.age !== undefined
            ? String(patient.age)
            : ""
        );

        setBiologicalSex(
          patient.biological_sex || ""
        );
      }

      setScreen("patient-history");
    } catch (error) {
      console.error(
        "Patient history error:",
        error
      );

      setHistoryError(
        error.message ||
          t.historyError
      );
    } finally {
      setLoadingHistory(false);
    }
  };

  const startNewVisit = () => {
    const patient =
      normalizeHistoryPatient(
        patientHistory,
        historyPatientId.trim()
      );

    if (patient) {
      setCreatedPatient(patient);

      if (patient.patient_id) {
        setHistoryPatientId(
          String(patient.patient_id)
        );
      }

      setPatientName(
        patient.patient_name || ""
      );

      setPatientAge(
        patient.age !== null &&
          patient.age !== undefined
          ? String(patient.age)
          : ""
      );

      setBiologicalSex(
        patient.biological_sex || ""
      );
    }

    setClinicalNote("");
    setTemperature("");
    setHeartRate("");
    setOxygenSaturation("");

    setCbcData({
      wbc: "",
      neutrophils: "",
      lymphocytes: "",
      hemoglobin: "",
      platelets: "",
    });

    if (xrayPreviewUrl) {
      URL.revokeObjectURL(
        xrayPreviewUrl
      );
    }

    setXrayFile(null);
    setXrayPreviewUrl(null);

    setAssessmentResult(null);
    setTreatmentPlan(null);
    setAssessmentError("");

    setAssistantMessages([]);
    setAssistantInput("");
    setAssistantError("");
    setAssistantLoading(false);

    setScreen("assessment");
  };

  // ============================================================
  // CBC
  // ============================================================

  const updateCbc = (
    field,
    value
  ) => {
    setCbcData((previous) => ({
      ...previous,
      [field]: value,
    }));
  };

  // ============================================================
  // RUN ASSESSMENT
  // ============================================================

  const runAssessment = async (event) => {
    event.preventDefault();

    setAssessmentError("");
    setAssessmentResult(null);
    setTreatmentPlan(null);

    setAssistantMessages([]);
    setAssistantInput("");
    setAssistantError("");
    setAssistantLoading(false);

    setRunningAssessment(true);

    try {
      if (!createdPatient?.patient_id) {
        throw new Error(t.noPatient);
      }

      if (!clinicalNote.trim()) {
        throw new Error(t.notesRequired);
      }

      if (!xrayFile) {
        throw new Error(t.xrayRequired);
      }

      const patientId =
        createdPatient.patient_id;

      const formData =
        new FormData();

      formData.append(
        "file",
        xrayFile
      );

      const xrayResponse =
        await fetch(
          `${API_BASE_URL}/api/patients/${patientId}/xray`,
          {
            method: "POST",
            body: formData,
          }
        );

      const xrayData =
        await xrayResponse.json();

      if (!xrayResponse.ok) {
        throw new Error(
          xrayData.detail
            ? typeof xrayData.detail ===
              "string"
              ? xrayData.detail
              : JSON.stringify(
                  xrayData.detail
                )
            : t.xrayRequired
        );
      }

      const payload = {
        patient_id: patientId,

        patient_name:
          createdPatient.patient_name ||
          patientName ||
          null,

        age:
          createdPatient.age !==
            undefined &&
          createdPatient.age !== null
            ? Number(
                createdPatient.age
              )
            : Number(patientAge),

        biological_sex:
          createdPatient.biological_sex ||
          biologicalSex ||
          null,

        temperature:
          temperature !== ""
            ? Number(temperature)
            : null,

        heart_rate:
          heartRate !== ""
            ? Number(heartRate)
            : null,

        oxygen_saturation:
          oxygenSaturation !== ""
            ? Number(
                oxygenSaturation
              )
            : null,

        clinical_notes:
          clinicalNote.trim(),
      };

      const cleanedCbc = {};

      Object.entries(
        cbcData
      ).forEach(
        ([key, value]) => {
          if (
            value !== "" &&
            value !== null &&
            value !== undefined &&
            !Number.isNaN(
              Number(value)
            )
          ) {
            cleanedCbc[key] =
              Number(value);
          }
        }
      );

      if (
        Object.keys(cleanedCbc)
          .length > 0
      ) {
        payload.cbc_data =
          cleanedCbc;
      }

      Object.keys(payload).forEach(
        (key) => {
          if (
            payload[key] === null
          ) {
            delete payload[key];
          }
        }
      );

      const response =
        await fetch(
          `${API_BASE_URL}/api/assessment`,
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/json",
            },
            body: JSON.stringify(
              payload
            ),
          }
        );

      const data =
        await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail
            ? typeof data.detail ===
              "string"
              ? data.detail
              : JSON.stringify(
                  data.detail
                )
            : data.error
              ? typeof data.error ===
                "string"
                ? data.error
                : JSON.stringify(
                    data.error
                  )
              : t.assessmentBackendError
        );
      }

      const assessmentWithPatient = {
        ...data,

        patient: {
          patient_id:
            patientId,

          patient_name:
            createdPatient.patient_name ||
            patientName ||
            null,

          age:
            createdPatient.age ??
            patientAge,

          biological_sex:
            createdPatient.biological_sex ||
            biologicalSex ||
            null,
        },

        xray: xrayData,
      };

      setAssessmentResult(
        assessmentWithPatient
      );

      // ========================================================
      // TREATMENT PLAN
      // ========================================================

      try {
        const assistantPayload = {
          question:
            lang === "ar"
              ? "ما العلاج الموصى به؟"
              : "What treatment is recommended?",

          language: lang,

          patient: {
            age: Number(
              assessmentWithPatient
                .patient.age
            ),

            age_unit: "years",

            sex:
              assessmentWithPatient
                .patient
                .biological_sex ||
              null,
          },

          assessment: {
            prediction:
              data?.result
                ?.prediction ??
              data?.prediction ??
              null,

            pneumonia_probability:
              data?.result
                ?.pneumonia_probability ??
              data?.fusion
                ?.pneumonia_probability ??
              null,

            oxygen_saturation:
              oxygenSaturation !== ""
                ? Number(
                    oxygenSaturation
                  )
                : null,

            clinical_notes:
              clinicalNote.trim(),

            temperature:
              temperature !== ""
                ? Number(
                    temperature
                  )
                : null,

            heart_rate:
              heartRate !== ""
                ? Number(
                    heartRate
                  )
                : null,

            fast_breathing:
              data?.fast_breathing ??
              data?.result
                ?.fast_breathing ??
              data?.severity
                ?.fast_breathing ??
              null,

            chest_indrawing:
              data?.chest_indrawing ??
              data?.result
                ?.chest_indrawing ??
              data?.severity
                ?.chest_indrawing ??
              null,

            general_danger_sign:
              data?.general_danger_sign ??
              data?.result
                ?.general_danger_sign ??
              data?.severity
                ?.general_danger_sign ??
              null,
          },

          visit: {
            age: Number(
              assessmentWithPatient
                .patient.age
            ),

            age_unit: "years",

            sex:
              assessmentWithPatient
                .patient
                .biological_sex ||
              null,

            prediction:
              data?.result
                ?.prediction ??
              data?.prediction ??
              null,

            pneumonia_probability:
              data?.result
                ?.pneumonia_probability ??
              data?.fusion
                ?.pneumonia_probability ??
              null,

            oxygen_saturation:
              oxygenSaturation !== ""
                ? Number(
                    oxygenSaturation
                  )
                : null,

            temperature:
              temperature !== ""
                ? Number(
                    temperature
                  )
                : null,

            heart_rate:
              heartRate !== ""
                ? Number(
                    heartRate
                  )
                : null,

            clinical_notes:
              clinicalNote.trim(),

            fast_breathing:
              data?.fast_breathing ??
              data?.result
                ?.fast_breathing ??
              data?.severity
                ?.fast_breathing ??
              null,

            chest_indrawing:
              data?.chest_indrawing ??
              data?.result
                ?.chest_indrawing ??
              data?.severity
                ?.chest_indrawing ??
              null,

            general_danger_sign:
              data?.general_danger_sign ??
              data?.result
                ?.general_danger_sign ??
              data?.severity
                ?.general_danger_sign ??
              null,
          },
        };

        const assistantResponse =
          await fetch(
            `${API_BASE_URL}/api/assistant/chat`,
            {
              method: "POST",
              headers: {
                "Content-Type":
                  "application/json",
              },
              body: JSON.stringify(
                assistantPayload
              ),
            }
          );

        const assistantData =
          await assistantResponse.json();

        if (
          assistantResponse.ok
        ) {
          setTreatmentPlan(
            assistantData?.treatment_plan ||
              null
          );
        } else {
          console.warn(
            "Treatment plan request failed:",
            assistantData
          );

          setTreatmentPlan(
            null
          );
        }
      } catch (
        treatmentError
      ) {
        console.warn(
          "Treatment plan request failed:",
          treatmentError
        );

        setTreatmentPlan(
          null
        );
      }
    } catch (error) {
      console.error(
        "PneumoCare AI assessment error:",
        error
      );

      setAssessmentError(
        error.message ||
          t.assessmentBackendError
      );
    } finally {
      setRunningAssessment(
        false
      );
    }
  };

  // ============================================================
  // AI ASSISTANT
  // ============================================================

  const askAssistant = async () => {
    const question =
      assistantInput.trim();

    if (!question) {
      return;
    }

    if (!assessmentResult) {
      return;
    }

    setAssistantError("");
    setAssistantLoading(true);

    const userMessage = {
      role: "user",
      content: question,
    };

    setAssistantMessages(
      (previous) => [
        ...previous,
        userMessage,
      ]
    );

    setAssistantInput("");

    try {
      const result =
        assessmentResult?.result ||
        {};

      const fusion =
        assessmentResult?.fusion ||
        {};

      const branches =
        assessmentResult?.branches ||
        {};

      const severity =
        assessmentResult?.severity ||
        {};

      const explanation =
        assessmentResult
          ?.decision_explanation ||
        {};

      const xai =
        assessmentResult?.xai ||
        {};

      const patient =
        assessmentResult?.patient ||
        createdPatient ||
        {};

      const assistantPayload = {
        question,
        language: lang,

        patient: {
          patient_id:
            patient?.patient_id ??
            null,

          patient_name:
            patient?.patient_name ??
            null,

          age:
            patient?.age !==
              undefined &&
            patient?.age !== null
              ? Number(
                  patient.age
                )
              : null,

          age_unit: "years",

          sex:
            patient?.biological_sex ??
            null,
        },

        assessment: {
          prediction:
            result?.prediction ??
            null,

          pneumonia_probability:
            result?.pneumonia_probability ??
            fusion?.pneumonia_probability ??
            null,

          normal_probability:
            result?.normal_probability ??
            null,

          clinical_notes:
            clinicalNote.trim(),

          temperature:
            temperature !== ""
              ? Number(
                  temperature
                )
              : null,

          heart_rate:
            heartRate !== ""
              ? Number(
                  heartRate
                )
              : null,

          oxygen_saturation:
            oxygenSaturation !== ""
              ? Number(
                  oxygenSaturation
                )
              : null,

          severity:
            severity?.severity ??
            null,

          high_risk_flags:
            severity?.high_risk_flags ??
            [],

          moderate_signals:
            severity?.moderate_signals ??
            [],

          conflict_detected:
            Boolean(
              explanation?.conflict_detected
            ),

          xray_prediction:
            branches?.xray
              ?.prediction ??
            xai?.prediction ??
            null,

          xray_pneumonia_probability:
            xai?.pneumonia_probability ??
            branches?.xray
              ?.pneumonia_probability ??
            null,

          clinical_prediction:
            branches
              ?.clinical_nlp
              ?.prediction ??
            null,

          vital_prediction:
            branches?.vital
              ?.prediction ??
            null,

          fast_breathing:
            assessmentResult
              ?.fast_breathing ??
            result?.fast_breathing ??
            severity?.fast_breathing ??
            null,

          chest_indrawing:
            assessmentResult
              ?.chest_indrawing ??
            result?.chest_indrawing ??
            severity?.chest_indrawing ??
            null,

          general_danger_sign:
            assessmentResult
              ?.general_danger_sign ??
            result?.general_danger_sign ??
            severity?.general_danger_sign ??
            null,
        },

        visit: {
          age:
            patient?.age !==
              undefined &&
            patient?.age !== null
              ? Number(
                  patient.age
                )
              : null,

          age_unit: "years",

          sex:
            patient?.biological_sex ??
            null,

          clinical_notes:
            clinicalNote.trim(),

          temperature:
            temperature !== ""
              ? Number(
                  temperature
                )
              : null,

          heart_rate:
            heartRate !== ""
              ? Number(
                  heartRate
                )
              : null,

          oxygen_saturation:
            oxygenSaturation !== ""
              ? Number(
                  oxygenSaturation
                )
              : null,

          cbc_data:
            cbcData,

          prediction:
            result?.prediction ??
            null,

          pneumonia_probability:
            result?.pneumonia_probability ??
            fusion?.pneumonia_probability ??
            null,

          severity:
            severity?.severity ??
            null,

          fast_breathing:
            assessmentResult
              ?.fast_breathing ??
            result?.fast_breathing ??
            severity?.fast_breathing ??
            null,

          chest_indrawing:
            assessmentResult
              ?.chest_indrawing ??
            result?.chest_indrawing ??
            severity?.chest_indrawing ??
            null,

          general_danger_sign:
            assessmentResult
              ?.general_danger_sign ??
            result?.general_danger_sign ??
            severity?.general_danger_sign ??
            null,
        },
      };

      const response =
        await fetch(
          `${API_BASE_URL}/api/assistant/chat`,
          {
            method: "POST",
            headers: {
              "Content-Type":
                "application/json",
            },
            body: JSON.stringify(
              assistantPayload
            ),
          }
        );

      let data = null;

      try {
        data =
          await response.json();
      } catch {
        data = null;
      }

      if (!response.ok) {
        const detail =
          data?.detail ||
          data?.error ||
          t.assistantError;

        throw new Error(
          typeof detail ===
            "string"
            ? detail
            : JSON.stringify(
                detail
              )
        );
      }

      const answer =
        data?.answer ??
        data?.assistant ??
        data?.response ??
        data?.message ??
        data?.text ??
        data?.reply ??
        data?.content ??
        data?.assistant_response ??
        data?.gemini_response ??
        data?.result?.answer ??
        data?.result?.response ??
        null;

      const fallbackAnswer =
        data?.treatment_plan
          ? lang === "ar"
            ? "تم إنشاء خطة علاجية منظمة بناءً على التقييم الحالي. راجع قسم خطة العلاج أدناه لمزيد من التفاصيل."
            : "A structured treatment plan was generated from the current assessment. Review the Treatment Plan section below for details."
          : null;

      const finalAnswer =
        answer ||
        fallbackAnswer;

      if (!finalAnswer) {
        throw new Error(
          t.assistantError
        );
      }

      setAssistantMessages(
        (previous) => [
          ...previous,
          {
            role: "assistant",
            content:
              typeof finalAnswer ===
              "string"
                ? finalAnswer
                : JSON.stringify(
                    finalAnswer
                  ),
          },
        ]
      );
    } catch (error) {
      console.error(
        "PneumoCare AI Assistant error:",
        error
      );

      setAssistantError(
        error.message ||
          t.assistantError
      );
    } finally {
      setAssistantLoading(
        false
      );
    }
  };

  const handleAssistantKeyDown = (
    event
  ) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      askAssistant();
    }
  };

  return (
    <div className="app-shell">
      <header className="navbar">
        <Brand t={t} />

        {screen === "home" && (
          <nav className="desktop-nav">
            <a href="#home">
              {t.home}
            </a>

            <a href="#features">
              {t.features}
            </a>

            <a href="#about">
              {t.about}
            </a>
          </nav>
        )}

        <div className="nav-actions">
          <LanguageSwitch
            lang={lang}
            onChange={
              switchLanguage
            }
          />

          <button
            className="nav-button"
            onClick={
              screen === "home"
                ? openAssessment
                : goHome
            }
          >
            {screen === "home"
              ? t.start
              : t.home}
          </button>
        </div>
      </header>

      {screen === "home" && (
        <Home
          t={t}
          openAssessment={
            openAssessment
          }
        />
      )}

      {screen ===
        "patient-selection" && (
        <PatientSelection
          t={t}
          openNewPatient={
            openNewPatient
          }
          openExistingPatient={
            openExistingPatient
          }
          goHome={goHome}
        />
      )}

      {screen === "new-patient" && (
        <NewPatient
          t={t}
          patientName={
            patientName
          }
          patientAge={
            patientAge
          }
          biologicalSex={
            biologicalSex
          }
          setPatientName={
            setPatientName
          }
          setPatientAge={
            setPatientAge
          }
          setBiologicalSex={
            setBiologicalSex
          }
          patientError={
            patientError
          }
          creatingPatient={
            creatingPatient
          }
          createPatient={
            createPatient
          }
          backToPatientSelection={
            backToPatientSelection
          }
        />
      )}

      {screen ===
        "existing-patient" && (
        <ExistingPatient
          t={t}
          historyPatientId={
            historyPatientId
          }
          setHistoryPatientId={
            setHistoryPatientId
          }
          loadPatientHistory={
            loadPatientHistory
          }
          loadingHistory={
            loadingHistory
          }
          historyError={
            historyError
          }
          backToPatientSelection={
            backToPatientSelection
          }
        />
      )}

      {screen ===
        "patient-history" && (
        <PatientHistory
          t={t}
          patientHistory={
            patientHistory
          }
          historyPatientId={
            historyPatientId
          }
          startNewVisit={
            startNewVisit
          }
          openExistingPatient={
            openExistingPatient
          }
          backToPatientSelection={
            backToPatientSelection
          }
        />
      )}

      {screen === "assessment" && (
        <Assessment
          t={t}
          createdPatient={
            createdPatient
          }
          clinicalNote={
            clinicalNote
          }
          setClinicalNote={
            setClinicalNote
          }
          temperature={
            temperature
          }
          setTemperature={
            setTemperature
          }
          heartRate={
            heartRate
          }
          setHeartRate={
            setHeartRate
          }
          oxygenSaturation={
            oxygenSaturation
          }
          setOxygenSaturation={
            setOxygenSaturation
          }
          cbcData={cbcData}
          updateCbc={
            updateCbc
          }
          xrayFile={
            xrayFile
          }
          setXrayFile={
            setXrayFile
          }
          xrayPreviewUrl={
            xrayPreviewUrl
          }
          setXrayPreviewUrl={
            setXrayPreviewUrl
          }
          runningAssessment={
            runningAssessment
          }
          assessmentError={
            assessmentError
          }
          runAssessment={
            runAssessment
          }
          setScreen={setScreen}
          assessmentResult={
            assessmentResult
          }
          treatmentPlan={
            treatmentPlan
          }
          assistantMessages={
            assistantMessages
          }
          assistantInput={
            assistantInput
          }
          setAssistantInput={
            setAssistantInput
          }
          assistantLoading={
            assistantLoading
          }
          assistantError={
            assistantError
          }
          askAssistant={
            askAssistant
          }
          handleAssistantKeyDown={
            handleAssistantKeyDown
          }
        />
      )}
    </div>
  );
}

// ============================================================
// LANGUAGE
// ============================================================

function LanguageSwitch({
  lang,
  onChange,
}) {
  return (
    <div
      className="language-switch"
      aria-label="Language selector"
    >
      <button
        className={
          lang === "en"
            ? "active"
            : ""
        }
        onClick={() =>
          onChange("en")
        }
      >
        English
      </button>

      <button
        className={
          lang === "ar"
            ? "active"
            : ""
        }
        onClick={() =>
          onChange("ar")
        }
      >
        العربية
      </button>
    </div>
  );
}

function Brand({ t }) {
  return (
    <div className="brand">
      <div className="brand-icon">
        P
      </div>

      <div>
        <h1>{t.brand}</h1>
        <span>{t.tagline}</span>
      </div>
    </div>
  );
}

// ============================================================
// HOME
// ============================================================

function Home({
  t,
  openAssessment,
}) {
  return (
    <>
      <main
        id="home"
        className="hero"
      >
        <div className="hero-content">
          <div className="badge">
            <span className="status-dot" />
            {t.aiSupport}
          </div>

          <h2>
            {t.heroTitle1}
            <br />
            <span>
              {t.heroTitle2}
            </span>
          </h2>

          <p className="hero-description">
            {t.heroText}
          </p>

          <div className="hero-actions">
            <button
              className="primary-button"
              onClick={
                openAssessment
              }
            >
              {t.start}{" "}
              <span>→</span>
            </button>

            <a
              href="#features"
              className="secondary-button"
            >
              {t.explore}
            </a>
          </div>

          <div className="trust-row">
            <div>
              <strong>
                {t.imaging}
              </strong>

              <span>
                {t.imagingText}
              </span>
            </div>

            <div>
              <strong>
                {t.clinical}
              </strong>

              <span>
                {t.clinicalText}
              </span>
            </div>

            <div>
              <strong>
                {t.vital}
              </strong>

              <span>
                {t.vitalText}
              </span>
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="glow" />

          <div className="medical-card">
            <div className="card-header">
              <span>
                {t.brand}
              </span>

              <span className="live">
                {t.production}
              </span>
            </div>

            <div className="lung-visual">
              <div className="lung lung-left" />
              <div className="lung lung-right" />
              <div className="scan-line" />
            </div>

            <div className="assessment-result">
              <div>
                <span>
                  {t.engineReady}
                </span>

                <strong>
                  {t.complete}
                </strong>
              </div>

              <div className="result-circle">
                AI
              </div>
            </div>
          </div>
        </div>
      </main>

      <section
        id="features"
        className="features"
      >
        <div className="section-heading">
          <span>
            {t.hybrid}
          </span>

          <h3>
            {t.featuresTitle}
          </h3>

          <p>
            {t.featuresText}
          </p>
        </div>

        <div className="feature-grid">
          <Feature
            icon="01"
            title={
              t.xrayFeature
            }
            text={
              t.xrayFeatureText
            }
          />

          <Feature
            icon="02"
            title={
              t.nlpFeature
            }
            text={
              t.nlpFeatureText
            }
          />

          <Feature
            icon="03"
            title={
              t.vitalFeature
            }
            text={
              t.vitalFeatureText
            }
          />
        </div>

        <div className="system-note">
          <strong>
            {t.safetyTitle}
          </strong>

          <span>
            {t.safetyShort}
          </span>
        </div>
      </section>

      <footer id="about">
        <div>
          <strong>
            {t.brand}
          </strong>

          <p>
            {t.fullTagline}
          </p>
        </div>

        <span>
          {t.release}
        </span>
      </footer>
    </>
  );
}

// ============================================================
// PATIENT SELECTION
// ============================================================

function PatientSelection({
  t,
  openNewPatient,
  openExistingPatient,
  goHome,
}) {
  return (
    <main className="page-wrap">
      <div className="page-heading">
        <div className="badge">
          <span className="status-dot" />
          {t.patientManagement}
        </div>

        <h2>
          {t.newAssessment}
        </h2>

        <p>
          {t.patientSelectionText}
        </p>
      </div>

      <div className="patient-options">
        <button
          className="patient-option-card"
          onClick={
            openNewPatient
          }
        >
          <div className="patient-option-icon">
            +
          </div>

          <div className="patient-option-content">
            <span className="option-label">
              {t.newPatient}
            </span>

            <h3>
              {t.createPatient}
            </h3>

            <p>
              {t.createPatientText}
            </p>

            <span className="option-arrow">
              {t.continue} →
            </span>
          </div>
        </button>

        <button
          className="patient-option-card"
          onClick={
            openExistingPatient
          }
        >
          <div className="patient-option-icon">
            ◉
          </div>

          <div className="patient-option-content">
            <span className="option-label">
              {t.existingPatient}
            </span>

            <h3>
              {t.openExisting}
            </h3>

            <p>
              {t.existingText}
            </p>

            <span className="option-arrow">
              {t.searchPatient} →
            </span>
          </div>
        </button>
      </div>

      <div className="patient-selection-footer">
        <span>🔒</span>
        {t.privacyNote}
      </div>

      <button
        className="text-back"
        onClick={goHome}
      >
        ← {t.home}
      </button>
    </main>
  );
}

// ============================================================
// EXISTING PATIENT
// ============================================================

function ExistingPatient({
  t,
  historyPatientId,
  setHistoryPatientId,
  loadPatientHistory,
  loadingHistory,
  historyError,
  backToPatientSelection,
}) {
  const [storedId, setStoredId] = useState("");

  // Always read last ID from localStorage when this screen opens
  useEffect(() => {
    let stored = "";
    try {
      stored =
        localStorage.getItem(
          "pneumocare_last_patient_id"
        ) || "";
    } catch {
      stored = "";
    }
    setStoredId(stored.trim());

    if (
      (!historyPatientId ||
        !String(historyPatientId).trim()) &&
      stored.trim()
    ) {
      setHistoryPatientId(stored.trim());
    }
  }, []); // run once on mount

  return (
    <main className="page-wrap narrow">
      <div className="page-heading">
        <div className="badge">
          <span className="status-dot" />
          {t.historyBadge}
        </div>

        <h2>
          {t.openExisting}
        </h2>

        <p>
          {t.historyIntro}
        </p>
      </div>

      <form
        className="patient-form"
        onSubmit={
          loadPatientHistory
        }
      >
        <div className="form-group">
          <label>
            {t.patientId}
          </label>

          <input
            type="text"
            value={
              historyPatientId || ""
            }
            onChange={(event) =>
              setHistoryPatientId(
                event.target.value
              )
            }
            placeholder={
              t.patientIdPlaceholder
            }
            required
            autoFocus
          />
        </div>

        {storedId ? (
          <div
            className="info-note"
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "12px",
              flexWrap: "wrap",
            }}
          >
            <span>
              <strong>{t.lastPatientId}:</strong>{" "}
              {storedId}
            </span>
            <button
              type="button"
              className="secondary-button"
              style={{
                minHeight: "36px",
                padding: "6px 12px",
                fontSize: "12px",
              }}
              onClick={() =>
                setHistoryPatientId(storedId)
              }
            >
              {t.useLastId}
            </button>
          </div>
        ) : null}

        {historyError && (
          <div className="error-box">
            {historyError}
          </div>
        )}

        <button
          className="primary-button full-button"
          type="submit"
          disabled={
            loadingHistory
          }
        >
          {loadingHistory
            ? t.loadingHistory
            : `${t.loadHistory} →`}
        </button>

        <button
          className="text-back"
          type="button"
          onClick={
            backToPatientSelection
          }
          disabled={
            loadingHistory
          }
        >
          ← {t.back}
        </button>
      </form>
    </main>
  );
}

// ============================================================
// PATIENT HISTORY
// ============================================================

function PatientHistory({
  t,
  patientHistory,
  historyPatientId,
  startNewVisit,
  openExistingPatient,
  backToPatientSelection,
}) {
  const patient =
    normalizeHistoryPatient(
      patientHistory,
      historyPatientId
    );

  const visits =
    normalizeHistoryVisits(
      patientHistory
    );

  return (
    <main className="page-wrap">
      <div className="page-heading">
        <div className="badge">
          <span className="status-dot" />
          {t.historyBadge}
        </div>

        <h2>
          {t.historyTitle}
        </h2>

        <p>
          {t.historyIntro}
        </p>
      </div>

      {/* Patient profile */}
      <section
        className="patient-summary-card"
        style={{
          marginBottom: "28px",
        }}
      >
        <div>
          <span>
            {t.patientId}
          </span>

          <strong>
            {patient?.patient_id ||
              historyPatientId ||
              "—"}
          </strong>
        </div>

        <div>
          <span>
            {t.patientName}
          </span>

          <strong>
            {patient?.patient_name ||
              "—"}
          </strong>
        </div>

        <div>
          <span>
            {t.age}
          </span>

          <strong>
            {patient?.age ??
              "—"}
          </strong>
        </div>

        <div>
          <span>
            {t.sex}
          </span>

          <strong>
            {translateSex(
              patient?.biological_sex,
              t
            )}
          </strong>
        </div>
      </section>

      {/* History header */}
      <section className="assessment-result-card">
        <div className="assessment-result-header">
          <span className="badge">
            <span className="status-dot" />
            {t.history}
          </span>

          <h3>
            {t.patientHistory}
          </h3>

          <p>
            {visits.length > 0
              ? `${visits.length} ${
                  visits.length ===
                  1
                    ? t.visit
                    : t.visits
                }`
              : t.noHistory}
          </p>
        </div>

        {visits.length > 0 ? (
          <div
            style={{
              display: "grid",
              gap: "18px",
            }}
          >
            {visits.map(
              (visit, index) => (
                <HistoryVisitCard
                  key={
                    visit.id ||
                    visit.visit_id ||
                    `visit-${index}`
                  }
                  visit={visit}
                  index={index}
                  t={t}
                />
              )
            )}
          </div>
        ) : (
          <div
            className="reasoning-card"
            style={{
              marginTop: "10px",
            }}
          >
            <div className="reasoning-icon">
              ℹ
            </div>

            <p>
              {t.noHistory}
            </p>
          </div>
        )}
      </section>

      <div
        className="assessment-actions"
        style={{
          marginTop: "28px",
        }}
      >
        <button
          type="button"
          className="secondary-button"
          onClick={
            openExistingPatient
          }
        >
          {t.viewHistory}
        </button>

        <button
          type="button"
          className="primary-button"
          onClick={
            startNewVisit
          }
        >
          + {t.newVisit}
        </button>
      </div>

      <button
        className="text-back"
        onClick={
          backToPatientSelection
        }
        style={{
          marginTop: "18px",
        }}
      >
        ← {t.back}
      </button>
    </main>
  );
}

// ============================================================
// HISTORY VISIT CARD
function HistoryVisitCard({
  visit,
  index,
  t,
}) {
  const [expanded, setExpanded] = useState(false);

  // ============================================================
  // BASIC VISIT DATA
  // ============================================================

  const result = visit?.result || {};
  const fusion = visit?.fusion || {};
  const severityData = visit?.severity || {};
  const treatment = visit?.treatment || {};
  const aiData = visit?.ai_clinical_reasoning || {};
  const aiReasoning = aiData?.reasoning || {};

  const prediction = getVisitPrediction(visit);

  const pneumoniaProbability =
    getVisitPneumoniaProbability(visit);

  const normalProbability =
    result?.normal_probability !== undefined &&
    result?.normal_probability !== null
      ? Number(result.normal_probability)
      : null;

  const clinicalNotes =
    visit?.clinical_notes ??
    visit?.clinical_note ??
    visit?.notes ??
    "";

  const temperature =
    visit?.temperature ??
    visit?.vitals?.temperature ??
    null;

  const heartRate =
    visit?.heart_rate ??
    visit?.vitals?.heart_rate ??
    null;

  const oxygenSaturation =
    visit?.oxygen_saturation ??
    visit?.spo2_pct ??
    visit?.vitals?.oxygen_saturation ??
    null;

  const visitDate =
    visit?.created_at ??
    visit?.assessment_date ??
    visit?.visit_date ??
    visit?.date ??
    null;

  // ============================================================
  // X-RAY INFORMATION
  // ============================================================

  const xray =
    visit?.xray ||
    visit?.xray_result ||
    visit?.imaging ||
    null;

  const xrayStructuredPrediction =
    xray?.prediction ??
    xray?.diagnosis ??
    xray?.result?.prediction ??
    xray?.result?.diagnosis ??
    null;

  const imagingInterpretation =
    aiReasoning?.imaging_interpretation ?? "";

  const xrayFinding =
    Array.isArray(aiReasoning?.key_findings)
      ? aiReasoning.key_findings.find((finding) =>
          /x-ray|xray/i.test(String(finding))
        )
      : "";

  const xrayText = String(
    xrayStructuredPrediction ||
      imagingInterpretation ||
      xrayFinding ||
      ""
  );

  const xraySaysPneumonia =
    /\b(?:x-ray|xray)\b[\s\S]*?\bpneumonia\b/i.test(
      xrayText
    ) ||
    (
      xrayStructuredPrediction &&
      String(xrayStructuredPrediction)
        .toLowerCase()
        .includes("pneumonia")
    );

  const xrayPneumoniaMatch =
    xrayText.match(
      /(?:x-ray|xray)[^.]*?(\d+(?:\.\d+)?)%\s*probability[^.]*pneumonia/i
    ) ||
    xrayText.match(
      /(?:x-ray|xray)[^.]*pneumonia[^.]*?(\d+(?:\.\d+)?)%/i
    );

  const xrayPneumoniaProbability =
    xrayPneumoniaMatch
      ? Number(xrayPneumoniaMatch[1])
      : null;

  const xrayPrediction =
    xrayStructuredPrediction ||
    (xraySaysPneumonia
      ? "Pneumonia"
      : null);

  // ============================================================
  // FUSION INFORMATION
  // ============================================================

  const fusionPrediction =
    fusion?.prediction ??
    prediction ??
    "Unknown";

  const fusionProbability =
    fusion?.pneumonia_probability !==
      undefined &&
    fusion?.pneumonia_probability !== null
      ? Number(fusion.pneumonia_probability)
      : pneumoniaProbability;

  const clinicalProbability =
    fusion?.inputs?.clinical_probability ??
    null;

  const vitalProbability =
    fusion?.inputs?.vital_probability ??
    null;

  const threshold =
    fusion?.threshold ??
    null;

  // ============================================================
  // CONFLICT
  // ============================================================

  const hasModalityConflict =
    Boolean(xrayPrediction) &&
    String(xrayPrediction)
      .toLowerCase()
      .includes("pneumonia") &&
    String(fusionPrediction)
      .toLowerCase() === "normal";

  // ============================================================
  // HELPERS
  // ============================================================

  const formatProbability = (value) => {
    if (
      value === null ||
      value === undefined ||
      Number.isNaN(Number(value))
    ) {
      return "—";
    }

    const numeric = Number(value);

    return `${(numeric <= 1
      ? numeric * 100
      : numeric
    ).toFixed(1)}%`;
  };

  const formatProbabilityExact = (value) => {
    if (
      value === null ||
      value === undefined ||
      Number.isNaN(Number(value))
    ) {
      return "—";
    }

    const numeric = Number(value);

    return `${(numeric <= 1
      ? numeric * 100
      : numeric
    ).toFixed(2)}%`;
  };

  const getReadablePrediction = (value) => {
    return translateHistoryPrediction(
      value,
      t
    );
  };

  // ============================================================
  // RENDER
  // ============================================================

  return (
    <div
      className="source-assessment-card"
      style={{
        width: "100%",
        boxSizing: "border-box",
      }}
    >
      {/* ========================================================
          VISIT HEADER
      ======================================================== */}

      <div className="source-card-header">
        <div>
          <span className="source-card-eyebrow">
            {t.visit} {index + 1}
          </span>

          <h5>
            {visitDate
              ? formatHistoryDate(visitDate)
              : "—"}
          </h5>
        </div>

        <span className="source-card-icon">
          {String(index + 1).padStart(2, "0")}
        </span>
      </div>

      {/* ========================================================
          QUICK UNDERSTANDING
      ======================================================== */}

      {hasModalityConflict ? (
        <div
          style={{
            marginTop: "18px",
            padding: "20px",
            borderRadius: "16px",
            background:
              "rgba(220, 120, 80, 0.08)",
            border:
              "1px solid rgba(220, 120, 80, 0.25)",
          }}
        >
          <div
            style={{
              fontSize: "0.72rem",
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              fontWeight: 800,
              opacity: 0.7,
            }}
          >
            Assessment Requires Clinical Review
          </div>

          <h4
            style={{
              margin: "8px 0 0",
              fontSize: "1.15rem",
              lineHeight: 1.4,
            }}
          >
            ⚠ Conflicting Results
          </h4>

          <p
            style={{
              margin: "9px 0 0",
              lineHeight: 1.7,
              opacity: 0.88,
            }}
          >
            The X-ray assessment indicates Pneumonia,
            while the clinical and vital assessment
            indicates a lower pneumonia probability.
            The two findings should be reviewed together
            by a qualified clinician.
          </p>
        </div>
      ) : (
        <div
          style={{
            marginTop: "18px",
            padding: "18px",
            borderRadius: "16px",
            background:
              "rgba(120, 140, 160, 0.06)",
          }}
        >
          <div className="source-card-eyebrow">
            Assessment Summary
          </div>

          <div
            style={{
              marginTop: "8px",
              fontSize: "1.15rem",
              fontWeight: 800,
            }}
          >
            {getReadablePrediction(
              prediction
            )}
          </div>

          {pneumoniaProbability !== null && (
            <div
              style={{
                marginTop: "5px",
                opacity: 0.75,
              }}
            >
              Pneumonia probability:{" "}
              <strong>
                {formatProbability(
                  pneumoniaProbability
                )}
              </strong>
            </div>
          )}
        </div>
      )}

      {/* ========================================================
          MAIN ASSESSMENT COMPARISON
      ======================================================== */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit, minmax(240px, 1fr))",
          gap: "14px",
          marginTop: "16px",
        }}
      >
        {/* X-RAY */}

        <div
          style={{
            padding: "18px",
            borderRadius: "14px",
            background:
              hasModalityConflict
                ? "rgba(220, 120, 80, 0.08)"
                : "rgba(120, 140, 160, 0.06)",
            border:
              hasModalityConflict
                ? "1px solid rgba(220, 120, 80, 0.22)"
                : "1px solid rgba(120, 140, 160, 0.12)",
          }}
        >
          <div className="source-card-eyebrow">
            X-Ray Assessment
          </div>

          {xrayPrediction ? (
            <>
              <div
                style={{
                  marginTop: "9px",
                  fontSize: "1.1rem",
                  fontWeight: 800,
                }}
              >
                {getReadablePrediction(
                  xrayPrediction
                )}
              </div>

              {xrayPneumoniaProbability !==
                null && (
                <div
                  style={{
                    marginTop: "5px",
                    fontSize: "0.9rem",
                    opacity: 0.75,
                  }}
                >
                  Pneumonia probability:{" "}
                  <strong>
                    {formatProbabilityExact(
                      xrayPneumoniaProbability
                    )}
                  </strong>
                </div>
              )}
            </>
          ) : (
            <div
              style={{
                marginTop: "9px",
                opacity: 0.6,
              }}
            >
              No X-ray assessment data available.
            </div>
          )}
        </div>

        {/* CLINICAL + VITAL */}

        <div
          style={{
            padding: "18px",
            borderRadius: "14px",
            background:
              "rgba(120, 140, 160, 0.06)",
            border:
              "1px solid rgba(120, 140, 160, 0.12)",
          }}
        >
          <div className="source-card-eyebrow">
            Clinical & Vital Assessment
          </div>

          <div
            style={{
              marginTop: "9px",
              fontSize: "1.1rem",
              fontWeight: 800,
            }}
          >
            {getReadablePrediction(
              fusionPrediction
            )}
          </div>

          {fusionProbability !== null && (
            <div
              style={{
                marginTop: "5px",
                fontSize: "0.9rem",
                opacity: 0.75,
              }}
            >
              Pneumonia probability:{" "}
              <strong>
                {formatProbabilityExact(
                  fusionProbability
                )}
              </strong>
            </div>
          )}
        </div>
      </div>

      {/* ========================================================
          SEVERITY - SHOW PROMINENTLY
      ======================================================== */}

      {severityData?.severity && (
        <div
          style={{
            marginTop: "16px",
            padding: "17px 18px",
            borderRadius: "14px",
            background:
              "rgba(120, 140, 160, 0.06)",
            border:
              "1px solid rgba(120, 140, 160, 0.12)",
          }}
        >
          <div className="source-card-eyebrow">
            Severity Assessment
          </div>

          <div
            style={{
              marginTop: "8px",
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "12px",
              flexWrap: "wrap",
            }}
          >
            <strong
              style={{
                fontSize: "1.05rem",
              }}
            >
              {String(
                severityData.severity
              )}
            </strong>

            {Array.isArray(
              severityData.high_risk_flags
            ) &&
              severityData.high_risk_flags.length >
                0 && (
                <span
                  style={{
                    fontSize: "0.85rem",
                    opacity: 0.8,
                  }}
                >
                  {severityData.high_risk_flags.join(
                    " • "
                  )}
                </span>
              )}
          </div>
        </div>
      )}

      {/* ========================================================
          VITALS
      ======================================================== */}

      {(temperature !== null ||
        heartRate !== null ||
        oxygenSaturation !== null) && (
        <div
          style={{
            marginTop: "18px",
            paddingTop: "18px",
            borderTop:
              "1px solid rgba(120, 140, 160, 0.14)",
          }}
        >
          <div className="source-card-eyebrow">
            {t.vitals}
          </div>

          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "10px",
              marginTop: "10px",
            }}
          >
            {temperature !== null && (
              <HistoryPill
                label={t.temperature}
                value={`${temperature} °C`}
              />
            )}

            {heartRate !== null && (
              <HistoryPill
                label={t.heartRate}
                value={`${heartRate} bpm`}
              />
            )}

            {oxygenSaturation !== null && (
              <HistoryPill
                label={t.oxygen}
                value={`${oxygenSaturation}%`}
              />
            )}
          </div>
        </div>
      )}

      {/* ========================================================
          CLINICAL NOTES
      ======================================================== */}

      {clinicalNotes && (
        <div
          style={{
            marginTop: "18px",
            paddingTop: "18px",
            borderTop:
              "1px solid rgba(120, 140, 160, 0.14)",
          }}
        >
          <div className="source-card-eyebrow">
            {t.clinicalNotes}
          </div>

          <p
            style={{
              margin: "8px 0 0",
              lineHeight: 1.7,
            }}
          >
            {clinicalNotes}
          </p>
        </div>
      )}

      {/* ========================================================
          FULL ASSESSMENT BUTTON
      ======================================================== */}

      <button
        type="button"
        onClick={() =>
          setExpanded((current) => !current)
        }
        style={{
          width: "100%",
          marginTop: "22px",
          padding: "13px 18px",
          borderRadius: "12px",
          border:
            "1px solid rgba(120, 140, 160, 0.2)",
          background:
            "rgba(120, 140, 160, 0.06)",
          color: "inherit",
          fontSize: "0.9rem",
          fontWeight: 700,
          cursor: "pointer",
        }}
      >
        {expanded
          ? "− Hide Full Assessment"
          : "＋ View Full Assessment"}
      </button>

      {/* ========================================================
          EXPANDED FULL ASSESSMENT
      ======================================================== */}

      {expanded && (
        <div
          style={{
            marginTop: "18px",
            display: "grid",
            gap: "16px",
          }}
        >
          {/* ----------------------------------------------------
              WHAT THE RESULTS MEAN
          ---------------------------------------------------- */}

          {hasModalityConflict && (
            <div
              style={{
                padding: "18px",
                borderRadius: "14px",
                background:
                  "rgba(120, 140, 160, 0.06)",
              }}
            >
              <div className="source-card-eyebrow">
                What Do These Results Mean?
              </div>

              <p
                style={{
                  margin: "10px 0 0",
                  lineHeight: 1.75,
                }}
              >
                The X-ray branch independently indicated
                Pneumonia with{" "}
                {xrayPneumoniaProbability !==
                null
                  ? formatProbabilityExact(
                      xrayPneumoniaProbability
                    )
                  : "a high probability"}
                . The clinical and vital branches
                produced a lower pneumonia probability.
                The X-ray result is independent evidence
                and is not included in the mathematical
                fusion shown below.
              </p>
            </div>
          )}

          {/* ----------------------------------------------------
              ASSESSMENT RESULT
          ---------------------------------------------------- */}

          <div
            style={{
              padding: "18px",
              borderRadius: "14px",
              background:
                "rgba(120, 140, 160, 0.06)",
            }}
          >
            <div className="source-card-eyebrow">
              Clinical & Vital Assessment
            </div>

            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit, minmax(180px, 1fr))",
                gap: "12px",
                marginTop: "12px",
              }}
            >
              <HistoryMetric
                label="Assessment"
                value={getReadablePrediction(
                  fusionPrediction
                )}
              />

              {fusionProbability !== null && (
                <HistoryMetric
                  label="Pneumonia Probability"
                  value={formatProbabilityExact(
                    fusionProbability
                  )}
                />
              )}

              {normalProbability !== null && (
                <HistoryMetric
                  label="Normal Probability"
                  value={formatProbabilityExact(
                    normalProbability
                  )}
                />
              )}
            </div>
          </div>

          {/* ----------------------------------------------------
              X-RAY DETAILS
          ---------------------------------------------------- */}

          {(xrayPrediction ||
            imagingInterpretation ||
            xrayFinding) && (
            <div
              style={{
                padding: "18px",
                borderRadius: "14px",
                background:
                  "rgba(120, 140, 160, 0.06)",
              }}
            >
              <div className="source-card-eyebrow">
                X-Ray Assessment
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns:
                    "repeat(auto-fit, minmax(180px, 1fr))",
                  gap: "12px",
                  marginTop: "12px",
                }}
              >
                {xrayPrediction && (
                  <HistoryMetric
                    label="X-Ray Prediction"
                    value={getReadablePrediction(
                      xrayPrediction
                    )}
                  />
                )}

                {xrayPneumoniaProbability !==
                  null && (
                  <HistoryMetric
                    label="X-Ray Pneumonia Probability"
                    value={formatProbabilityExact(
                      xrayPneumoniaProbability
                    )}
                  />
                )}
              </div>

              {imagingInterpretation && (
                <p
                  style={{
                    margin: "14px 0 0",
                    lineHeight: 1.75,
                    opacity: 0.88,
                  }}
                >
                  {imagingInterpretation}
                </p>
              )}
            </div>
          )}

          {/* ----------------------------------------------------
              FUSION DETAILS
          ---------------------------------------------------- */}

          {Object.keys(fusion).length > 0 && (
            <div
              style={{
                padding: "18px",
                borderRadius: "14px",
                background:
                  "rgba(120, 140, 160, 0.06)",
              }}
            >
              <div className="source-card-eyebrow">
                Clinical & Vital Evidence
              </div>

              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "10px",
                  marginTop: "12px",
                }}
              >
                {fusion.engine && (
                  <HistoryPill
                    label="Engine"
                    value={fusion.engine}
                  />
                )}

                {clinicalProbability !== null && (
                  <HistoryPill
                    label="Clinical Probability"
                    value={formatProbabilityExact(
                      clinicalProbability
                    )}
                  />
                )}

                {vitalProbability !== null && (
                  <HistoryPill
                    label="Vital Probability"
                    value={formatProbabilityExact(
                      vitalProbability
                    )}
                  />
                )}

                {fusionProbability !== null && (
                  <HistoryPill
                    label="Fusion Probability"
                    value={formatProbabilityExact(
                      fusionProbability
                    )}
                  />
                )}

                {threshold !== null && (
                  <HistoryPill
                    label="Decision Threshold"
                    value={String(threshold)}
                  />
                )}
              </div>

              {fusion.weights &&
                typeof fusion.weights ===
                  "object" && (
                  <div
                    style={{
                      marginTop: "10px",
                      display: "flex",
                      flexWrap: "wrap",
                      gap: "10px",
                    }}
                  >
                    {Object.entries(
                      fusion.weights
                    ).map(
                      ([key, value]) => (
                        <HistoryPill
                          key={key}
                          label={`${formatHistoryLabel(
                            key
                          )} Weight`}
                          value={formatProbability(
                            value
                          )}
                        />
                      )
                    )}
                  </div>
                )}
            </div>
          )}

          {/* ----------------------------------------------------
              SEVERITY DETAILS
          ---------------------------------------------------- */}

          {Object.keys(severityData).length >
            0 && (
            <div
              style={{
                padding: "18px",
                borderRadius: "14px",
                background:
                  "rgba(120, 140, 160, 0.06)",
              }}
            >
              <div className="source-card-eyebrow">
                Severity Assessment
              </div>

              <div
                style={{
                  display: "flex",
                  flexWrap: "wrap",
                  gap: "10px",
                  marginTop: "12px",
                }}
              >
                {severityData.severity && (
                  <HistoryPill
                    label="Severity"
                    value={String(
                      severityData.severity
                    )}
                  />
                )}

                {severityData.score !==
                  undefined &&
                  severityData.score !== null && (
                    <HistoryPill
                      label="Score"
                      value={String(
                        severityData.score
                      )}
                    />
                  )}

                {severityData.clinical_status && (
                  <HistoryPill
                    label="Clinical Status"
                    value={String(
                      severityData.clinical_status
                    )}
                  />
                )}
              </div>

              {Array.isArray(
                severityData.high_risk_flags
              ) &&
                severityData.high_risk_flags.length >
                  0 && (
                  <div
                    style={{
                      marginTop: "15px",
                    }}
                  >
                    <div className="source-card-eyebrow">
                      High-Risk Signals
                    </div>

                    <ul
                      style={{
                        margin: "8px 0 0",
                        paddingLeft: "20px",
                        lineHeight: 1.8,
                      }}
                    >
                      {severityData.high_risk_flags.map(
                        (flag, flagIndex) => (
                          <li key={flagIndex}>
                            {flag}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}

              {Array.isArray(
                severityData.moderate_signals
              ) &&
                severityData.moderate_signals.length >
                  0 && (
                  <div
                    style={{
                      marginTop: "15px",
                    }}
                  >
                    <div className="source-card-eyebrow">
                      Moderate Signals
                    </div>

                    <ul
                      style={{
                        margin: "8px 0 0",
                        paddingLeft: "20px",
                        lineHeight: 1.8,
                      }}
                    >
                      {severityData.moderate_signals.map(
                        (
                          signal,
                          signalIndex
                        ) => (
                          <li key={signalIndex}>
                            {signal}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}
            </div>
          )}

          {/* ----------------------------------------------------
              TREATMENT / CLINICAL GUIDANCE
          ---------------------------------------------------- */}

          {Object.keys(treatment).length > 0 && (
            <div
              style={{
                padding: "18px",
                borderRadius: "14px",
                background:
                  "rgba(120, 140, 160, 0.06)",
              }}
            >
              <div className="source-card-eyebrow">
                Clinical Guidance
              </div>

              {Array.isArray(
                treatment.recommendations
              ) &&
                treatment.recommendations.length >
                  0 && (
                  <ul
                    style={{
                      margin: "12px 0 0",
                      paddingLeft: "20px",
                      lineHeight: 1.8,
                    }}
                  >
                    {treatment.recommendations.map(
                      (
                        recommendation,
                        recommendationIndex
                      ) => (
                        <li
                          key={
                            recommendationIndex
                          }
                        >
                          {recommendation}
                        </li>
                      )
                    )}
                  </ul>
                )}

              {Array.isArray(
                treatment.alerts
              ) &&
                treatment.alerts.length > 0 && (
                  <div
                    style={{
                      marginTop: "14px",
                    }}
                  >
                    {treatment.alerts.map(
                      (alert, alertIndex) => (
                        <HistoryPill
                          key={alertIndex}
                          label="Alert"
                          value={alert}
                        />
                      )
                    )}
                  </div>
                )}
            </div>
          )}

          {/* ----------------------------------------------------
              GEMINI CLINICAL REASONING
          ---------------------------------------------------- */}

          {Object.keys(aiReasoning).length >
            0 && (
            <div
              style={{
                padding: "18px",
                borderRadius: "14px",
                background:
                  "rgba(120, 140, 160, 0.06)",
              }}
            >
              <div className="source-card-eyebrow">
                Clinical Reasoning
              </div>

              {aiReasoning.summary && (
                <p
                  style={{
                    margin: "11px 0 0",
                    lineHeight: 1.75,
                  }}
                >
                  {aiReasoning.summary}
                </p>
              )}

              {Array.isArray(
                aiReasoning.key_findings
              ) &&
                aiReasoning.key_findings.length >
                  0 && (
                  <div
                    style={{
                      marginTop: "16px",
                    }}
                  >
                    <div className="source-card-eyebrow">
                      Key Findings
                    </div>

                    <ul
                      style={{
                        margin: "8px 0 0",
                        paddingLeft: "20px",
                        lineHeight: 1.8,
                      }}
                    >
                      {aiReasoning.key_findings.map(
                        (finding, findingIndex) => (
                          <li key={findingIndex}>
                            {finding}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}

              {aiReasoning.risk_interpretation && (
                <div
                  style={{
                    marginTop: "16px",
                  }}
                >
                  <div className="source-card-eyebrow">
                    Risk Interpretation
                  </div>

                  <p
                    style={{
                      margin: "8px 0 0",
                      lineHeight: 1.75,
                    }}
                  >
                    {
                      aiReasoning.risk_interpretation
                    }
                  </p>
                </div>
              )}

              {aiReasoning.clinical_cautions &&
                Array.isArray(
                  aiReasoning.clinical_cautions
                ) &&
                aiReasoning.clinical_cautions.length >
                  0 && (
                  <div
                    style={{
                      marginTop: "16px",
                    }}
                  >
                    <div className="source-card-eyebrow">
                      Clinical Considerations
                    </div>

                    <ul
                      style={{
                        margin: "8px 0 0",
                        paddingLeft: "20px",
                        lineHeight: 1.8,
                      }}
                    >
                      {aiReasoning.clinical_cautions.map(
                        (caution, cautionIndex) => (
                          <li key={cautionIndex}>
                            {caution}
                          </li>
                        )
                      )}
                    </ul>
                  </div>
                )}

              {aiReasoning.recommended_review && (
                <div
                  style={{
                    marginTop: "16px",
                  }}
                >
                  <div className="source-card-eyebrow">
                    Recommended Review
                  </div>

                  <p
                    style={{
                      margin: "8px 0 0",
                      lineHeight: 1.75,
                    }}
                  >
                    {
                      aiReasoning.recommended_review
                    }
                  </p>
                </div>
              )}

              {aiReasoning.disclaimer && (
                <div
                  style={{
                    marginTop: "16px",
                    paddingTop: "14px",
                    borderTop:
                      "1px solid rgba(120, 140, 160, 0.14)",
                    fontSize: "0.85rem",
                    opacity: 0.7,
                    lineHeight: 1.6,
                  }}
                >
                  {aiReasoning.disclaimer}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
function HistoryMetric({
  label,
  value,
}) {
  return (
    <div
      style={{
        padding:
          "14px 16px",
        borderRadius:
          "12px",
        background:
          "rgba(120, 140, 160, 0.06)",
      }}
    >
      <span
        style={{
          display:
            "block",
          fontSize:
            "0.72rem",
          textTransform:
            "uppercase",
          letterSpacing:
            "0.08em",
          opacity: 0.65,
          marginBottom:
            "6px",
        }}
      >
        {label}
      </span>

      <strong>
        {value}
      </strong>
    </div>
  );
}

function HistoryPill({
  label,
  value,
}) {
  return (
    <div
      style={{
        padding:
          "9px 12px",
        borderRadius:
          "10px",
        background:
          "rgba(120, 140, 160, 0.06)",
        fontSize:
          "0.86rem",
      }}
    >
      <strong>
        {label}:{" "}
      </strong>
      <span>
        {value}
      </span>
    </div>
  );
}

// ============================================================
// NEW PATIENT
// ============================================================

function NewPatient({
  t,
  patientName,
  patientAge,
  biologicalSex,
  setPatientName,
  setPatientAge,
  setBiologicalSex,
  patientError,
  creatingPatient,
  createPatient,
  backToPatientSelection,
}) {
  return (
    <main className="page-wrap narrow">
      <div className="page-heading">
        <div className="badge">
          <span className="status-dot" />
          {t.newPatientBadge}
        </div>

        <h2>
          {t.createCase}
        </h2>

        <p>
          {t.basicInfo}
        </p>
      </div>

      <form
        className="patient-form"
        onSubmit={
          createPatient
        }
      >
        <div className="form-group">
          <label>
            {t.patientName}
          </label>

          <input
            type="text"
            value={
              patientName
            }
            onChange={(e) =>
              setPatientName(
                e.target.value
              )
            }
            placeholder={
              t.enterPatientName
            }
            required
          />
        </div>

        <div className="form-group">
          <label>
            {t.age}
          </label>

          <input
            type="number"
            value={
              patientAge
            }
            onChange={(e) =>
              setPatientAge(
                e.target.value
              )
            }
            placeholder={
              t.enterAge
            }
            min="0"
            max="18"
            step="0.1"
            required
          />
        </div>

        <div className="form-group">
          <label>
            {t.sex}
          </label>

          <select
            value={
              biologicalSex
            }
            onChange={(e) =>
              setBiologicalSex(
                e.target.value
              )
            }
            required
          >
            <option value="">
              {t.selectSex}
            </option>

            <option value="Male">
              {t.male}
            </option>

            <option value="Female">
              {t.female}
            </option>
          </select>
        </div>

        {patientError && (
          <div className="error-box">
            {patientError}
          </div>
        )}

        <button
          className="primary-button full-button"
          type="submit"
          disabled={
            creatingPatient
          }
        >
          {creatingPatient
            ? t.creating
            : `${t.createCaseButton} →`}
        </button>

        <button
          className="text-back"
          type="button"
          onClick={
            backToPatientSelection
          }
        >
          ← {t.back}
        </button>
      </form>
    </main>
  );
}

// ============================================================
// ASSESSMENT
// ============================================================

function Assessment(props) {
  const {
    t,
    createdPatient,
    clinicalNote,
    setClinicalNote,
    temperature,
    setTemperature,
    heartRate,
    setHeartRate,
    oxygenSaturation,
    setOxygenSaturation,
    cbcData,
    updateCbc,
    xrayFile,
    setXrayFile,
    xrayPreviewUrl,
    setXrayPreviewUrl,
    runningAssessment,
    assessmentError,
    runAssessment,
    setScreen,
    assessmentResult,
    treatmentPlan,
    assistantMessages,
    assistantInput,
    setAssistantInput,
    assistantLoading,
    assistantError,
    askAssistant,
    handleAssistantKeyDown,
  } = props;

  return (
    <main className="assessment-page">
      <div className="page-heading">
        <div className="badge">
          <span className="status-dot" />
          {t.assessmentBadge}
        </div>

        <h2>
          {t.assessmentTitle}
        </h2>

        <p>
          {t.assessmentText}
        </p>
      </div>

      {createdPatient && (
        <div className="patient-summary-card">
          <div>
            <span>
              {t.patientId}
            </span>

            <strong>
              {
                createdPatient.patient_id
              }
            </strong>
          </div>

          <div>
            <span>
              {t.patientName}
            </span>

            <strong>
              {createdPatient.patient_name ||
                "—"}
            </strong>
          </div>

          <div>
            <span>
              {t.age}
            </span>

            <strong>
              {createdPatient.age ??
                "—"}
            </strong>
          </div>

          <div>
            <span>
              {t.sex}
            </span>

            <strong>
              {translateSex(
                createdPatient.biological_sex,
                t
              )}
            </strong>
          </div>
        </div>
      )}

      <form
        className="assessment-form"
        onSubmit={
          runAssessment
        }
      >
        <section className="assessment-section">
          <SectionHeader
            number="01"
            title={
              t.clinicalInfo
            }
            description={
              t.clinicalInfoDesc
            }
          />

          <div className="assessment-grid">
            <Input
              label={
                t.temperature
              }
              type="number"
              step="0.1"
              value={
                temperature
              }
              onChange={
                setTemperature
              }
              placeholder="38.5"
            />

            <Input
              label={
                t.heartRate
              }
              type="number"
              value={
                heartRate
              }
              onChange={
                setHeartRate
              }
              placeholder="105"
            />

            <Input
              label={
                t.oxygen
              }
              type="number"
              step="0.1"
              value={
                oxygenSaturation
              }
              onChange={
                setOxygenSaturation
              }
              placeholder="94"
            />
          </div>

          <div className="form-group">
            <label>
              {t.clinicalNotes}{" "}
              <span className="required">
                *
              </span>
            </label>

            <textarea
              value={
                clinicalNote
              }
              onChange={(e) =>
                setClinicalNote(
                  e.target.value
                )
              }
              placeholder={
                t.notesPlaceholder
              }
              rows="7"
              required
            />
          </div>
        </section>

        <section className="assessment-section">
          <SectionHeader
            number="02"
            title={t.cbc}
            description={
              t.cbcDesc
            }
          />

          <div className="assessment-grid">
            <Input
              label={t.wbc}
              value={
                cbcData.wbc
              }
              onChange={(v) =>
                updateCbc(
                  "wbc",
                  v
                )
              }
              placeholder="WBC"
            />

            <Input
              label={
                t.neutrophils
              }
              value={
                cbcData.neutrophils
              }
              onChange={(v) =>
                updateCbc(
                  "neutrophils",
                  v
                )
              }
              placeholder="%"
            />

            <Input
              label={
                t.lymphocytes
              }
              value={
                cbcData.lymphocytes
              }
              onChange={(v) =>
                updateCbc(
                  "lymphocytes",
                  v
                )
              }
              placeholder="%"
            />

            <Input
              label={
                t.hemoglobin
              }
              value={
                cbcData.hemoglobin
              }
              onChange={(v) =>
                updateCbc(
                  "hemoglobin",
                  v
                )
              }
              placeholder="g/dL"
            />

            <Input
              label={
                t.platelets
              }
              value={
                cbcData.platelets
              }
              onChange={(v) =>
                updateCbc(
                  "platelets",
                  v
                )
              }
              placeholder="Platelets"
            />
          </div>

          <div className="info-note">
            {t.cbcNote}
          </div>
        </section>

        <section className="assessment-section">
          <SectionHeader
            number="03"
            title={
              t.chestXray
            }
            description={
              t.xrayDesc
            }
          />

          <div className="xray-upload">
            <input
              id="xray-upload"
              type="file"
              accept="image/png,image/jpeg,image/jpg,image/webp,.png,.jpg,.jpeg,.webp"
              onChange={(e) => {
                const file =
                  e.target.files?.[0] ||
                  null;

                setXrayFile(
                  file
                );

                if (
                  xrayPreviewUrl
                ) {
                  URL.revokeObjectURL(
                    xrayPreviewUrl
                  );
                }

                if (file) {
                  const preview =
                    URL.createObjectURL(
                      file
                    );

                  setXrayPreviewUrl(
                    preview
                  );
                } else {
                  setXrayPreviewUrl(
                    null
                  );
                }
              }}
              required
            />

            <label htmlFor="xray-upload">
              <span className="upload-icon">
                ↑
              </span>

              <strong>
                {t.upload}
              </strong>

              <small>
                {t.formats}
              </small>
            </label>
          </div>

          {xrayFile && (
            <div className="file-selected">
              <span>✓</span>

              <div>
                <strong>
                  {
                    xrayFile.name
                  }
                </strong>

                <small>
                  {t.selected}
                </small>
              </div>
            </div>
          )}
        </section>

        {assessmentError && (
          <div className="error-box">
            <strong>
              {t.assessmentError}
            </strong>

            <p>
              {assessmentError}
            </p>
          </div>
        )}

        <div className="assessment-actions">
          <button
            type="button"
            className="secondary-button"
            onClick={() =>
              setScreen(
                "patient-selection"
              )
            }
            disabled={
              runningAssessment
            }
          >
            {t.cancel}
          </button>

          <button
            type="submit"
            className="primary-button"
            disabled={
              runningAssessment ||
              !createdPatient?.patient_id
            }
          >
            {runningAssessment
              ? t.running
              : `${t.runAssessment} →`}
          </button>
        </div>
      </form>

      {assessmentResult && (
        <AssessmentResult
          result={
            assessmentResult
          }
          t={t}
          xrayPreviewUrl={
            xrayPreviewUrl
          }
          treatmentPlan={
            treatmentPlan
          }
          assistantMessages={
            assistantMessages
          }
          assistantInput={
            assistantInput
          }
          setAssistantInput={
            setAssistantInput
          }
          assistantLoading={
            assistantLoading
          }
          assistantError={
            assistantError
          }
          askAssistant={
            askAssistant
          }
          handleAssistantKeyDown={
            handleAssistantKeyDown
          }
        />
      )}
    </main>
  );
}

// ============================================================
// INPUT
// ============================================================

function Input({
  label,
  value,
  onChange,
  ...props
}) {
  return (
    <div className="form-group">
      <label>{label}</label>

      <input
        value={value}
        onChange={(e) =>
          onChange(
            e.target.value
          )
        }
        {...props}
      />
    </div>
  );
}

// ============================================================
// SECTION HEADER
// ============================================================

function SectionHeader({
  number,
  title,
  description,
}) {
  return (
    <div className="assessment-section-header">
      <span className="section-number">
        {number}
      </span>

      <div>
        <h3>{title}</h3>

        <p>
          {description}
        </p>
      </div>
    </div>
  );
}

// ============================================================
// FEATURE
// ============================================================

function Feature({
  icon,
  title,
  text,
}) {
  return (
    <div className="feature-card">
      <div className="feature-number">
        {icon}
      </div>

      <h4>{title}</h4>

      <p>{text}</p>

      <span className="arrow">
        →
      </span>
    </div>
  );
}

// ============================================================
// ASSESSMENT RESULT
// ============================================================

function AssessmentResult({
  result,
  t,
  xrayPreviewUrl,
  treatmentPlan,
  assistantMessages,
  assistantInput,
  setAssistantInput,
  assistantLoading,
  assistantError,
  askAssistant,
  handleAssistantKeyDown,
}) {
  const final =
    result?.result || {};

  const fusion =
    result?.fusion || {};

  const branches =
    result?.branches || {};

  const severity =
    result?.severity || {};

  const explanation =
    result?.decision_explanation ||
    {};

  const xai =
    result?.xai || {};

  const isPneumonia =
    final.prediction ===
    "Pneumonia";

  const pneumoniaProbability =
    Number(
      final.pneumonia_probability ??
        fusion.pneumonia_probability ??
        0
    );

  const normalProbability =
    Number(
      final.normal_probability ??
        1 -
          pneumoniaProbability
    );

  const xrayProbability =
    Number(
      xai?.pneumonia_probability ??
        branches?.xray
          ?.pneumonia_probability ??
        0
    );

  const clinicalFinalPrediction =
    final.prediction ??
    fusion.prediction ??
    "Unknown";

  const clinicalFinalPneumonia =
    Number(
      fusion.pneumonia_probability ??
        final.pneumonia_probability ??
        pneumoniaProbability
    );

  const clinicalFinalNormal =
    Number(
      fusion.normal_probability ??
        final.normal_probability ??
        1 -
          clinicalFinalPneumonia
    );

  const xrayPrediction =
    xai?.prediction ??
    branches?.xray?.prediction ??
    "Unknown";

  const xrayNormalProbability =
    Number(
      xai?.normal_probability ??
        branches?.xray
          ?.normal_probability ??
        1 -
          xrayProbability
    );

  const conflictDetected =
    Boolean(
      explanation?.conflict_detected
    );

  const apiBase =
    API_BASE_URL.replace(
      /\/$/,
      ""
    );

  const xaiUrl = xai?.url
    ? `${apiBase}${xai.url}`
    : null;

  const uploadedXrayUrl =
    xrayPreviewUrl || null;

  const riskLevel =
    String(
      severity?.severity ||
        (pneumoniaProbability >=
        0.665
          ? "moderate"
          : "low")
    ).toLowerCase();

  const translatePrediction = (
    prediction
  ) => {
    if (
      prediction ===
      "Pneumonia"
    ) {
      return t.pneumonia;
    }

    if (
      prediction ===
      "Normal"
    ) {
      return t.normal;
    }

    return (
      prediction ||
      t.unknown
    );
  };

  return (
    <section className="assessment-result-card">
      <div className="assessment-result-header">
        <span className="badge">
          <span className="status-dot" />
          {t.complete}
        </span>

        <h3>
          {t.resultTitle}
        </h3>

        <p>
          {t.resultText}
        </p>
      </div>

      <div className="final-result-panel">
        <div>
          <span className="result-label">
            {t.overall}
          </span>

          <h4 className="overall-risk-title">
            {t.risk}:{" "}
            <strong>
              {formatPercent(
                pneumoniaProbability
              )}
            </strong>
          </h4>

          <p className="overall-risk-context">
            {t.overallRiskContext}
          </p>

          <p className="overall-normal-secondary">
            {t.normalLikelihood}:{" "}
            <strong>
              {formatPercent(
                normalProbability
              )}
            </strong>
          </p>
        </div>

        <div className="probability-ring">
          <strong>
            {formatPercent(
              pneumoniaProbability
            )}
          </strong>

          <span>
            {t.risk}
          </span>
        </div>
      </div>

      <div className="probability-grid">
        <ProbabilityCard
          label={t.risk}
          value={
            pneumoniaProbability
          }
          emphasis={
            isPneumonia
          }
        />

        <ProbabilityCard
          label={
            t.normalLikelihood
          }
          value={
            normalProbability
          }
          emphasis={
            !isPneumonia
          }
        />

        <div className="probability-card">
          <span>
            {t.riskLevel}
          </span>

          <strong
            className={`risk-text ${riskLevel}`}
          >
            {translateRisk(
              riskLevel,
              t
            )}
          </strong>

          <div className="risk-description">
            {riskLevel ===
            "low"
              ? t.noHighRisk
              : t.considerationsTitle}
          </div>
        </div>
      </div>

      <ResultSection
        eyebrow={t.evidence}
        title={
          t.evidenceTitle
        }
      >
        <p className="section-intro">
          {t.xraySeparate}
        </p>

        <div className="source-assessment-grid">
          <div className="source-assessment-card clinical-source-card">
            <div className="source-card-header">
              <div>
                <span className="source-card-eyebrow">
                  {t.clinicalFinal}
                </span>

                <h5>
                  {translatePrediction(
                    clinicalFinalPrediction
                  )}
                </h5>
              </div>

              <span className="source-card-icon">
                CL
              </span>
            </div>

            <p className="source-card-description">
              {t.clinicalSources}
            </p>

            <div className="source-probability-list">
              <ProbabilityRow
                label={
                  t.pneumoniaProbability
                }
                value={
                  clinicalFinalPneumonia
                }
                positive
              />

              <ProbabilityRow
                label={
                  t.normalProbability
                }
                value={
                  clinicalFinalNormal
                }
              />
            </div>

            <div className="source-inputs-row">
              <span>
                {branches?.clinical_nlp?.available
                  ? `✓ ${t.clinicalEvidence}`
                  : `• ${t.clinicalEvidence}: ${t.unavailable}`}
              </span>

              <span>
                {branches?.vital?.available
                  ? `✓ ${t.vitalEvidence}`
                  : `• ${t.vitalEvidence}: ${t.unavailable}`}
              </span>

              <span>
                ✓ {t.cbc}
              </span>
            </div>

            <div className="source-estimate-note">
              {t.sourceEstimateNote}
            </div>
          </div>

          <div className="source-assessment-card xray-source-card">
            <div className="source-card-header">
              <div>
                <span className="source-card-eyebrow">
                  {t.xrayFinal}
                </span>

                <h5>
                  {translatePrediction(
                    xrayPrediction
                  )}
                </h5>
              </div>

              <span className="source-card-icon">
                XR
              </span>
            </div>

            <p className="source-card-description">
              {t.xraySource}
            </p>

            <div className="source-probability-list">
              <ProbabilityRow
                label={
                  t.pneumoniaProbability
                }
                value={
                  xrayProbability
                }
                positive
              />

              <ProbabilityRow
                label={
                  t.normalProbability
                }
                value={
                  xrayNormalProbability
                }
              />
            </div>

            <div className="source-inputs-row">
              <span>
                {branches?.xray?.available ||
                xai?.prediction
                  ? `✓ ${t.analyzed}`
                  : `• ${t.unavailable}`}
              </span>

              <span>
                {translatePrediction(
                  xrayPrediction
                )}
              </span>
            </div>

            <div className="source-estimate-note">
              {t.sourceEstimateNote}
            </div>
          </div>
        </div>
      </ResultSection>

      <ResultSection
        eyebrow={
          t.reasoning
        }
        title={
          t.reasoningTitle
        }
      >
        <div className="reasoning-card">
          <div className="reasoning-icon">
            ✓
          </div>

          <p>
            {t.reasoningText}
          </p>
        </div>
      </ResultSection>

      {conflictDetected && (
        <div className="conflict-banner">
          <div className="conflict-icon">
            !
          </div>

          <div>
            <strong>
              {t.conflictTitle}
            </strong>

            <p>
              {t.conflictText}
            </p>
          </div>
        </div>
      )}

      <ResultSection
        eyebrow={
          t.imagingExplanation
        }
        title={
          t.imagingTitle
        }
      >
        <p className="section-intro">
          {t.imagingText}
        </p>

        {xaiUrl ? (
          <>
            <div className="xai-image-grid">
              <div className="xai-image-card">
                <div className="xai-image-label">
                  {t.originalXray}
                </div>

                {uploadedXrayUrl ? (
                  <div className="xai-image-frame">
                    <img
                      src={
                        uploadedXrayUrl
                      }
                      alt={
                        t.originalXray
                      }
                    />
                  </div>
                ) : (
                  <div className="xai-image-placeholder">
                    {
                      t.imageUnavailable
                    }
                  </div>
                )}
              </div>

              <div className="xai-image-card">
                <div className="xai-image-label">
                  {t.attentionMap}
                </div>

                <div className="xai-image-frame">
                  <img
                    src={xaiUrl}
                    alt={
                      t.attentionMap
                    }
                  />
                </div>
              </div>
            </div>

            <div className="xai-metrics">
              <div>
                <span>
                  {t.prediction}
                </span>

                <strong>
                  {translatePrediction(
                    xai?.prediction ||
                      branches
                        .xray
                        ?.prediction
                  )}
                </strong>
              </div>

              <div>
                <span>
                  {t.likelihood}
                </span>

                <strong>
                  {formatPercent(
                    xrayProbability
                  )}
                </strong>
              </div>
            </div>
          </>
        ) : (
          <div className="xai-unavailable">
            <strong>
              {t.gradUnavailable}
            </strong>
          </div>
        )}

        {xai?.interpretation && (
          <div className="xai-disclaimer">
            <strong>
              {t.interpretation}
            </strong>

            <p>
              {
                xai.interpretation
              }
            </p>
          </div>
        )}
      </ResultSection>

      <ResultSection
        eyebrow={
          t.severitySection
        }
        title={
          t.severityTitle
        }
      >
        <div className="severity-card">
          <div>
            <span>
              {t.severityLevel}
            </span>

            <strong
              className={`severity-${riskLevel}`}
            >
              {translateRisk(
                riskLevel,
                t
              )}
            </strong>
          </div>

          <div className="severity-signals">
            <span>
              {t.signals}
            </span>

            <p>
              {severity
                .high_risk_flags
                ?.length
                ? severity.high_risk_flags.join(
                    ", "
                  )
                : severity
                    .moderate_signals
                    ?.length
                  ? severity.moderate_signals.join(
                      ", "
                    )
                  : t.noHighRisk}
            </p>
          </div>
        </div>
      </ResultSection>

      <TreatmentPlanCard
        treatmentPlan={
          treatmentPlan
        }
        t={t}
      />

      <AssistantCard
        t={t}
        messages={
          assistantMessages
        }
        input={
          assistantInput
        }
        setInput={
          setAssistantInput
        }
        loading={
          assistantLoading
        }
        error={
          assistantError
        }
        onAsk={
          askAssistant
        }
        onKeyDown={
          handleAssistantKeyDown
        }
      />

      <div className="safety-banner">
        <div className="safety-icon">
          !
        </div>

        <div>
          <strong>
            {t.safetyTitle}
          </strong>

          <p>
            {t.safetyText}
          </p>
        </div>
      </div>
    </section>
  );
}

// ============================================================
// ASSISTANT
// ============================================================

function AssistantCard({
  t,
  messages,
  input,
  setInput,
  loading,
  error,
  onAsk,
  onKeyDown,
}) {
  return (
    <ResultSection
      eyebrow={
        t.assistant
      }
      title={
        t.assistantTitle
      }
    >
      <div className="assistant-card">
        <div className="assistant-header">
          <div className="assistant-icon">
            AI
          </div>

          <div>
            <strong>
              {t.assistantTitle}
            </strong>

            <p>
              {t.assistantIntro}
            </p>
          </div>
        </div>

        <div className="assistant-messages">
          {messages.length ===
            0 && (
            <div className="assistant-message assistant-message-ai">
              <div className="assistant-message-label">
                {t.assistantAI}
              </div>

              <p>
                {
                  t.assistantWelcome
                }
              </p>
            </div>
          )}

          {messages.map(
            (
              message,
              index
            ) => (
              <div
                key={`${message.role}-${index}`}
                className={`assistant-message ${
                  message.role ===
                  "user"
                    ? "assistant-message-user"
                    : "assistant-message-ai"
                }`}
              >
                <div className="assistant-message-label">
                  {message.role ===
                  "user"
                    ? t.assistantYou
                    : t.assistantAI}
                </div>

                <p>
                  {
                    message.content
                  }
                </p>
              </div>
            )
          )}

          {loading && (
            <div className="assistant-message assistant-message-ai assistant-loading">
              <div className="assistant-message-label">
                {t.assistantAI}
              </div>

              <p>
                {
                  t.assistantThinking
                }
              </p>

              <div className="assistant-dots">
                <span />
                <span />
                <span />
              </div>
            </div>
          )}
        </div>

        {error && (
          <div className="assistant-error">
            <strong>
              {t.assistantError}
            </strong>

            <p>
              {error}
            </p>
          </div>
        )}

        <div className="assistant-compose">
          <div className="assistant-compose-heading">
            <span className="assistant-compose-icon">
              ✦
            </span>

            <div>
              <strong>
                {t.assistantTitle}
              </strong>

              <span>
                {
                  t.assistantPlaceholder
                }
              </span>
            </div>
          </div>

          <div className="assistant-input-row">
            <textarea
              value={input}
              onChange={(
                event
              ) =>
                setInput(
                  event.target
                    .value
                )
              }
              onKeyDown={
                onKeyDown
              }
              placeholder={
                t.assistantPlaceholder
              }
              rows="2"
              disabled={
                loading
              }
              aria-label={
                t.assistantPlaceholder
              }
            />

            <button
              type="button"
              className="primary-button assistant-send-button"
              onClick={onAsk}
              disabled={
                loading ||
                !input.trim()
              }
            >
              <span>
                {loading
                  ? "..."
                  : "✦"}
              </span>

              {loading
                ? "..."
                : t.assistantSend}
            </button>
          </div>
        </div>
      </div>
    </ResultSection>
  );
}

// ============================================================
// TREATMENT PLAN
// ============================================================

function TreatmentPlanCard({
  treatmentPlan,
  t,
}) {
  if (!treatmentPlan) {
    return null;
  }

  const status =
    String(
      treatmentPlan.status ||
        treatmentPlan.clinical_status ||
        ""
    ).toUpperCase();

  const medications =
    normalizeArray(
      treatmentPlan.medications ??
        treatmentPlan.medication ??
        treatmentPlan.recommended_medications
    );

  const supportiveCare =
    normalizeArray(
      treatmentPlan.supportive_care ??
        treatmentPlan.supportiveCare ??
        treatmentPlan.supportive
    );

  const monitoring =
    normalizeArray(
      treatmentPlan.monitoring ??
        treatmentPlan.monitoring_plan
    );

  const redFlags =
    normalizeArray(
      treatmentPlan.red_flags ??
        treatmentPlan.redFlags ??
        treatmentPlan.warning_signs
    );

  const clinicianReview =
    treatmentPlan.clinician_review ??
    treatmentPlan.clinicianReview ??
    treatmentPlan.review_required;

  const evidenceSource =
    treatmentPlan.evidence_source ??
    treatmentPlan.source ??
    null;

  const statusConfig =
    getTreatmentStatus(
      status,
      t
    );

  const hasAnyContent =
    medications.length > 0 ||
    supportiveCare.length > 0 ||
    monitoring.length > 0 ||
    redFlags.length > 0;

  return (
    <ResultSection
      eyebrow={t.treatment}
      title={
        t.treatmentTitle
      }
    >
      <div className="treatment-plan-card">
        <div className="treatment-plan-header">
          <div>
            <span className="treatment-plan-label">
              {t.clinicalStatus}
            </span>

            <h5>
              {
                statusConfig.label
              }
            </h5>
          </div>

          <span
            className={`treatment-status treatment-status-${statusConfig.className}`}
          >
            {
              statusConfig.shortLabel
            }
          </span>
        </div>

        <p className="treatment-plan-intro">
          {t.treatmentIntro}
        </p>

        {hasAnyContent ? (
          <div className="treatment-plan-grid">
            <TreatmentBlock
              title={
                t.medications
              }
              icon="Rx"
              items={
                medications
              }
              emptyText={
                t.noMedication
              }
              medication
            />

            <TreatmentBlock
              title={
                t.supportiveCare
              }
              icon="+"
              items={
                supportiveCare
              }
              emptyText={
                t.noSupportiveCare
              }
            />

            <TreatmentBlock
              title={
                t.monitoring
              }
              icon="◉"
              items={
                monitoring
              }
              emptyText={
                t.noMonitoring
              }
            />

            <TreatmentBlock
              title={
                t.redFlags
              }
              icon="!"
              items={
                redFlags
              }
              emptyText={
                t.noRedFlags
              }
            />
          </div>
        ) : (
          <div className="treatment-empty-state">
            <div className="treatment-empty-icon">
              ℹ
            </div>

            <div>
              <strong>
                {
                  t.treatmentUnavailable
                }
              </strong>

              <p>
                {
                  t.treatmentDisclaimer
                }
              </p>
            </div>
          </div>
        )}

        <div className="treatment-review">
          <div className="treatment-review-icon">
            ✓
          </div>

          <div>
            <strong>
              {
                t.clinicianReview
              }
            </strong>

            <p>
              {typeof clinicianReview ===
              "string"
                ? clinicianReview
                : t.treatmentDisclaimer}
            </p>
          </div>
        </div>

        <div className="treatment-safety-note">
          {t.medicationSafety}
        </div>

        <div className="treatment-source">
          <span>
            {t.evidenceSource}
          </span>

          <strong>
            {evidenceSource ||
              t.whoGuideline}
          </strong>
        </div>
      </div>
    </ResultSection>
  );
}

function TreatmentBlock({
  title,
  icon,
  items,
  emptyText,
  medication = false,
}) {
  return (
    <div
      className={`treatment-block ${
        medication
          ? "treatment-medication-block"
          : ""
      }`}
    >
      <div className="treatment-block-header">
        <span className="treatment-block-icon">
          {icon}
        </span>

        <h6>
          {title}
        </h6>
      </div>

      {items.length > 0 ? (
        <div className="treatment-items">
          {items.map(
            (
              item,
              index
            ) => (
              <div
                className="treatment-item"
                key={`${String(
                  item
                )}-${index}`}
              >
                <span>
                  •
                </span>

                <p>
                  {cleanTreatmentText(
                    item
                  )}
                </p>
              </div>
            )
          )}
        </div>
      ) : (
        <p className="treatment-empty">
          {emptyText}
        </p>
      )}
    </div>
  );
}

// ============================================================
// GENERIC HELPERS
// ============================================================

function normalizeArray(
  value
) {
  if (Array.isArray(value)) {
    return value.filter(
      (item) =>
        item !== null &&
        item !== undefined &&
        String(item).trim() !== ""
    );
  }

  if (
    value !== null &&
    value !== undefined &&
    String(value).trim() !== ""
  ) {
    return [value];
  }

  return [];
}

function cleanTreatmentText(
  value
) {
  if (
    value &&
    typeof value ===
      "object"
  ) {
    return (
      value.name ||
      value.medication ||
      value.label ||
      value.description ||
      JSON.stringify(
        value
      )
    );
  }

  return String(value);
}

function getTreatmentStatus(
  status,
  t
) {
  if (status === "URGENT") {
    return {
      className: "urgent",
      label: t.urgent,
      shortLabel: t.urgent,
    };
  }

  if (
    status ===
      "CLINICIAN_REVIEW" ||
    status ===
      "REVIEW_REQUIRED"
  ) {
    return {
      className: "review",
      label:
        t.clinicianReviewStatus,
      shortLabel:
        t.clinicianReviewStatus,
    };
  }

  if (
    status ===
    "RECOMMENDED"
  ) {
    return {
      className:
        "recommended",
      label:
        t.recommended,
      shortLabel:
        t.recommended,
    };
  }

  return {
    className: "review",
    label:
      t.clinicianReviewStatus,
    shortLabel:
      t.clinicianReviewStatus,
  };
}

function ResultSection({
  eyebrow,
  title,
  children,
}) {
  return (
    <div className="result-section">
      <div className="result-section-title">
        <span>
          {eyebrow}
        </span>

        <h4>
          {title}
        </h4>
      </div>

      {children}
    </div>
  );
}

function SimpleBranchCard({
  title,
  prediction,
  available,
  t,
}) {
  return (
    <div className="branch-card">
      <div className="branch-card-top">
        <span>
          {title}
        </span>

        <span
          className={`branch-status ${
            available
              ? "analyzed"
              : ""
          }`}
        >
          {available
            ? t.analyzed
            : t.unavailable}
        </span>
      </div>

      <h5>
        {prediction ===
        "Pneumonia"
          ? t.pneumonia
          : prediction ===
              "Normal"
            ? t.normal
            : t.unknown}
      </h5>
    </div>
  );
}

function ProbabilityRow({
  label,
  value,
  positive = false,
}) {
  const numericValue =
    Math.min(
      1,
      Math.max(
        0,
        Number(value) || 0
      )
    );

  return (
    <div className="source-probability-row">
      <div className="source-probability-top">
        <span>
          {label}
        </span>

        <strong>
          {formatPercent(
            numericValue
          )}
        </strong>
      </div>

      <div className="source-probability-track">
        <div
          className={`source-probability-fill ${
            positive
              ? "pneumonia-fill"
              : "normal-fill"
          }`}
          style={{
            width: `${numericValue * 100}%`,
          }}
        />
      </div>
    </div>
  );
}

function ProbabilityCard({
  label,
  value,
  emphasis,
}) {
  return (
    <div
      className={`probability-card ${
        emphasis
          ? "probability-emphasis"
          : ""
      }`}
    >
      <span>
        {label}
      </span>

      <strong>
        {formatPercent(
          value
        )}
      </strong>

      <div className="probability-bar">
        <div
          className="probability-bar-fill"
          style={{
            width: `${Math.min(
              100,
              Math.max(
                0,
                Number(value) *
                  100
              )
            )}%`,
          }}
        />
      </div>
    </div>
  );
}

function translateRisk(
  level,
  t
) {
  if (level === "high") {
    return t.high;
  }

  if (
    level ===
    "moderate"
  ) {
    return t.moderate;
  }

  return t.low;
}

function formatPercent(
  value
) {
  const numericValue =
    Number(value);

  if (
    Number.isNaN(
      numericValue
    )
  ) {
    return "0.0%";
  }

  return `${(
    numericValue * 100
  ).toFixed(1)}%`;
}

// ============================================================
// HISTORY HELPERS
// ============================================================

function firstNonEmpty(
  ...values
) {
  for (const value of values) {
    if (
      value !== null &&
      value !== undefined &&
      value !== ""
    ) {
      return value;
    }
  }

  return null;
}

function normalizeHistoryPatient(
  data,
  fallbackId = ""
) {
  const candidate =
    data?.patient ||
    data?.patient_data ||
    data?.patientData ||
    data?.data?.patient ||
    data?.data?.patient_data ||
    data?.profile ||
    null;

  if (
    candidate &&
    typeof candidate ===
      "object"
  ) {
    return {
      patient_id:
        candidate.patient_id ??
        candidate.patientId ??
        candidate.id ??
        fallbackId,

      patient_name:
        candidate.patient_name ??
        candidate.patientName ??
        candidate.name ??
        candidate.full_name ??
        "",

      age:
        candidate.age ??
        candidate.age_years ??
        candidate.patient_age ??
        null,

      biological_sex:
        candidate.biological_sex ??
        candidate.biologicalSex ??
        candidate.sex ??
        candidate.gender ??
        "",
    };
  }

  return {
    patient_id:
      fallbackId,
    patient_name: "",
    age: null,
    biological_sex: "",
  };
}

function normalizeHistoryVisits(
  data
) {
  if (Array.isArray(data)) {
    return data;
  }

  const possibleArrays = [
    data?.history,
    data?.visits,
    data?.assessments,
    data?.clinical_history,
    data?.clinicalHistory,
    data?.data?.history,
    data?.data?.visits,
    data?.data?.assessments,
    data?.patient?.history,
    data?.patient?.visits,
  ];

  for (
    const candidate of possibleArrays
  ) {
    if (
      Array.isArray(
        candidate
      )
    ) {
      return candidate;
    }
  }

  return [];
}

function getVisitPrediction(
  visit
) {
  return (
    visit?.prediction ??
    visit?.assessment?.prediction ??
    visit?.result?.prediction ??
    visit?.result?.diagnosis ??
    visit?.fusion?.prediction ??
    visit?.xray?.prediction ??
    visit?.xray_result?.prediction ??
    "Unknown"
  );
}

function getVisitPneumoniaProbability(
  visit
) {
  const value =
    visit?.pneumonia_probability ??
    visit?.assessment?.pneumonia_probability ??
    visit?.result?.pneumonia_probability ??
    visit?.fusion?.pneumonia_probability ??
    visit?.assessment_result?.pneumonia_probability ??
    null;

  if (
    value === null ||
    value === undefined ||
    value === ""
  ) {
    return null;
  }

  const numeric =
    Number(value);

  if (
    Number.isNaN(
      numeric
    )
  ) {
    return null;
  }

  // Handles both 0.85 and 85 formats.
  return numeric > 1
    ? numeric / 100
    : numeric;
}

function getVisitSeverity(
  visit
) {
  return (
    visit?.severity?.severity ??
    visit?.severity ??
    visit?.assessment?.severity ??
    visit?.result?.severity ??
    null
  );
}

function translateHistoryPrediction(
  prediction,
  t
) {
  const normalized =
    String(
      prediction || ""
    ).toLowerCase();

  if (
    normalized.includes(
      "pneumonia"
    )
  ) {
    return t.pneumonia;
  }

  if (
    normalized === "normal"
  ) {
    return t.normal;
  }

  if (
    !prediction ||
    normalized ===
      "unknown"
  ) {
    return t.unknown;
  }

  return String(
    prediction
  );
}

function translateSex(
  sex,
  t
) {
  if (
    String(sex)
      .toLowerCase() ===
    "male"
  ) {
    return t.male;
  }

  if (
    String(sex)
      .toLowerCase() ===
    "female"
  ) {
    return t.female;
  }

  return t.unknown;
}

function formatHistoryDate(
  value
) {
  try {
    const date =
      new Date(value);

    if (
      Number.isNaN(
        date.getTime()
      )
    ) {
      return String(value);
    }

    return date.toLocaleString();
  } catch {
    return String(value);
  }
}

function formatHistoryLabel(
  key
) {
  return String(key)
    .replace(
      /_/g,
      " "
    )
    .replace(
      /\b\w/g,
      (letter) =>
        letter.toUpperCase()
    );
}

function formatHistoryValue(
  value
) {
  if (
    value === null ||
    value === undefined
  ) {
    return "—";
  }

  if (
    typeof value ===
    "object"
  ) {
    return JSON.stringify(
      value
    );
  }

  return String(value);
}

export default App;