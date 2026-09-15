# PneumoCare AI

### Intelligent Pneumonia Assessment & Clinical Decision Support

PneumoCare AI is a multimodal clinical decision-support prototype designed to assist with the assessment of **pediatric community-acquired pneumonia (CAP)** across the pediatric age range.

The system integrates heterogeneous clinical evidence, including **clinical notes, structured patient information, vital signs, laboratory/CBC evidence, and chest X-ray analysis**, together with explainable AI, evidence fusion, retrieval-augmented generation (RAG), and clinical decision-support functionality.

> **Important:** PneumoCare AI is a research and clinical decision-support prototype. It is not a replacement for professional medical judgment and must not be used as an autonomous diagnostic or prescribing system.

---

## 1. Overview

Pediatric community-acquired pneumonia assessment can require the integration of multiple evidence sources rather than relying on a single signal.

PneumoCare AI is designed around a multimodal workflow:

```text
                         Patient Record
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Clinical Notes     Vital / CBC      Chest X-Ray
             │                │                │
             ▼                ▼                ▼
        NLP Evidence     Structured Evidence   Image AI
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                      Evidence Analysis
                              │
                  ┌───────────┴───────────┐
                  │                       │
                  ▼                       ▼
         Clinical/Vital Evidence     X-Ray Evidence
                  │                       │
                  └───────────┬───────────┘
                              ▼
                   Explainable Assessment
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
           ▼                  ▼                  ▼
        Severity         Clinical Safety    Treatment Support
           │                  │                  │
           └──────────────────┼──────────────────┘
                              ▼
                        AI Assistant
```

---

## 2. Main Features

### Patient Management

* Create and manage patient records.
* Store demographic and clinical information.
* Record visits and assessments.
* Maintain patient assessment history.
* Support repeated assessments for the same patient.

### Multimodal Assessment

The system integrates multiple evidence categories:

* Clinical notes
* Vital signs
* CBC / laboratory information
* Structured patient information
* Chest X-ray evidence

### X-Ray Analysis

The imaging branch provides:

* Pneumonia-related image classification
* Independent X-ray evidence
* Grad-CAM explainability
* Visual interpretation support

### Explainable AI

PneumoCare AI provides interpretable supporting evidence rather than displaying only a final prediction.

For chest X-rays, the system uses **Grad-CAM** to highlight image regions associated with the model output.

### Conflict Awareness

When different evidence sources do not strongly agree, the system can display a **Conflict Warning** so that the discrepancy can be reviewed by the clinician.

### Clinical Decision Support

The application can provide:

* Pneumonia Risk
* AI Evidence
* X-Ray Evidence
* Grad-CAM
* Conflict Warning
* Severity
* Clinical Considerations
* Clinical Safety
* Treatment Plan

### AI Clinical Assistant

The integrated assistant supports questions about:

* The current patient assessment
* X-ray findings
* Evidence conflicts
* Treatment-related questions
* General medical information

The assistant supports both **English and Arabic**, including question-language detection and intent-aware routing.

---

## 3. System Architecture

```text
React Frontend
      │
      ▼
FastAPI Backend
      │
      ├──────── Patient Management
      ├──────── Assessment APIs
      ├──────── X-Ray Processing
      ├──────── Clinical / Vital Processing
      ├──────── Laboratory Evidence
      ├──────── Evidence Fusion
      ├──────── Explainability
      └──────── AI Assistant
                     │
                     ├──── Intent Router
                     ├──── RAG Retrieval
                     ├──── Clinical Reasoning
                     └──── Treatment Engine
```

---

## 4. Evidence Fusion Configuration

The current production clinical/vital evidence fusion uses fixed configuration values:

| Parameter                                           | Current Configuration |
| --------------------------------------------------- | --------------------: |
| CLIN-NOTE weight                                    |              **0.73** |
| VITAL-FUSE weight                                   |              **0.27** |
| Decision threshold                                  |             **0.665** |
| X-Ray included in clinical/vital probability fusion |                **No** |

### Fusion Interpretation

```text
CLIN-NOTE  ── 0.73 ──┐
                     ├── Clinical/Vital Evidence Fusion
VITAL-FUSE ── 0.27 ──┘
```

The X-ray branch remains an **independent evidence source**.

It is not numerically inserted into the final clinical/vital probability fusion used by the current production engine.

The weights and threshold are fixed deployment configuration values. They are not dynamically searched or optimized during application startup.

---

## 5. AI Components

### 5.1 Clinical / NLP Branch

A ClinicalBERT-based pipeline is used to process clinical text and extract clinically relevant evidence.

The NLP workflow is designed to handle variability in medical language across different pediatric ages and clinical-note styles.

This is particularly relevant to pediatric settings, where descriptions may differ between infants, young children, and adolescents.

### 5.2 Vital / Structured Clinical Branch

Structured patient information and physiological evidence are processed through the vital evidence pipeline.

The current implementation supports the structured variables required by the production evidence-fusion workflow.

### 5.3 Laboratory / CBC Branch

Laboratory evidence includes CBC-related variables and inflammatory markers.

Documented project features include:

* WBC
* Neutrophils / NEU
* Lymphocytes
* Monocytes
* Platelets
* CRP
* NLR
* MPV
* RDW

Laboratory evidence is processed as structured clinical information and contributes to the project's clinical evidence workflow.

### 5.4 X-Ray Branch

The imaging branch uses a **ResNet50-based** architecture for chest X-ray analysis.

The branch provides both prediction output and explainability through Grad-CAM.

### 5.5 Evidence Fusion

The current production configuration uses:

* **0.73 CLIN-NOTE**
* **0.27 VITAL-FUSE**
* **0.665 decision threshold**

The X-ray branch is intentionally maintained as an independent evidence source for interpretation and explainability.

---

# 6. Dataset Sources

PneumoCare AI was developed using heterogeneous medical data collected from **multiple public datasets, published resources, clinical-note sources, laboratory resources, project-prepared datasets, and project-specific clinical information**.

The datasets are not treated as one single homogeneous training population.

Different datasets support different modalities, experiments, preprocessing pipelines, and evaluation tasks.

---

## 6.1 Chest X-Ray Data

### VinDr-PCXR

VinDr-PCXR is a pediatric chest X-ray dataset used for pediatric imaging development and evaluation.

Documented project information includes:

* **9,125 chest X-ray studies**
* Pediatric patients younger than 10 years
* Hospital-acquired pediatric chest imaging
* Image-level disease labels
* Lesion-level annotations

The published dataset has its own official organization, while project experiments apply additional preprocessing and experiment-specific handling.

### Kermany et al. Pneumonia Dataset

The Kermany pediatric pneumonia dataset contains:

* **5,863 labeled chest X-ray images**
* Normal and Pneumonia categories
* Primarily pediatric cases
* Strong relevance to pneumonia image classification

This dataset was used as an additional imaging source for pneumonia-related development and benchmarking.

### NIH ChestXray-14

NIH ChestXray-14 provides a large-scale chest X-ray resource.

Within the project documentation, it is used selectively to extend coverage toward the adolescent age range, particularly:

* Approximately **11–18 years**
* Additional pediatric/adolescent imaging coverage
* Cross-source preprocessing and evaluation support

### Additional Imaging Preparation

The imaging workflow includes experiment-specific:

* Filtering
* Resizing
* Normalization
* Quality preparation
* Class balancing where required
* Source-aware evaluation
* Train / validation / test handling

The source datasets are therefore not assumed to have identical distributions.

---

# 7. Laboratory and CBC Data

The laboratory component was developed using more than one source.

## 7.1 Güven & Kışlal (2022)

The project documentation references pediatric laboratory information covering:

* Approximately **800 children**
* Approximately **3 months–18 years**
* CBC and inflammatory laboratory parameters

Documented variables include:

* WBC
* Neutrophils
* Lymphocytes
* Monocytes
* Platelets
* CRP
* NLR
* MPV
* RDW

This resource supports the design of the laboratory evidence pipeline.

## 7.2 ERS Congress 2024 – OA1992

The documented project source includes:

* **509 children**
* Approximately **2–18 years**
* Children with confirmed community-acquired pneumonia
* WBC
* NEU
* CRP
* NLR

This provides additional clinically relevant laboratory evidence for pediatric CAP.

## 7.3 Project-Prepared Laboratory Data

The project also includes structured and prepared laboratory data used in machine-learning experiments and evidence processing.

Where synthetic or transformed laboratory data are used, they are treated as **experimental model-development resources** and are not represented as independent prospective clinical cohorts.

---

# 8. Clinical Notes and Medical Text

The clinical NLP component uses multiple clinical-text resources.

## 8.1 NoteChat

NoteChat provides synthetic doctor–patient conversations derived from clinical information.

It supports:

* Conversational clinical language
* Patient–doctor dialogue
* Informal clinical descriptions
* Clinical NLP experimentation

The project documentation includes pediatric examples.

## 8.2 PMC-Patients

PMC-Patients provides clinical case information derived from PubMed Central case reports.

It contributes:

* Clinical case summaries
* Medical terminology
* Clinical writing patterns
* Patient-condition descriptions

## 8.3 Augmented Clinical Notes

The project uses augmented clinical-note resources combining multiple clinical-text sources and structured information.

The documented resource includes combinations of:

* PMC-Patients
* NoteChat-derived conversations
* Structured patient information
* Clinical summaries

The public augmented resource contains approximately **30,000 note/conversation/summary triplets**.

## 8.4 MIMIC-IV Demo

MIMIC-IV Demo is used primarily as a clinical-text and discharge-summary style reference.

It supports:

* Clinical documentation style
* Medical terminology
* Structured discharge-summary patterns
* Realistic clinical-text formatting

## 8.5 Additional Project-Prepared Clinical Notes

Additional clinical-note samples were prepared and normalized for:

* Preprocessing
* NLP experiments
* RAG retrieval
* Assistant testing
* Clinical reasoning
* Intent classification

The project report explicitly documents **NoteChat, Augmented Clinical Notes, and MIMIC-IV Demo** within the clinical-notes component.

---

# 9. Clinical / Hospital Data

The project documentation also identifies clinical information associated with the:

**Respiratory Hospital and Pulmonary Care in Suez**

This project-specific clinical context is considered separately from public benchmark datasets.

Hospital-associated or project-specific information is not automatically assumed to be patient-linked with the public imaging or laboratory datasets.

---

# 10. Multimodal Data Types

The project integrates four major categories of evidence:

| Modality                     | Examples                                           |
| ---------------------------- | -------------------------------------------------- |
| **Imaging**                  | Chest X-ray                                        |
| **Clinical Text**            | Medical notes, clinical dialogue, case summaries   |
| **Laboratory**               | CBC, WBC, NEU, CRP, NLR and related markers        |
| **Structured Clinical Data** | Age, vital signs, symptoms and patient information |

The overall workflow is:

```text
                    MULTIPLE DATA SOURCES
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
     Imaging             Laboratory        Clinical Notes
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                            ▼
                  Modality-specific
                    preprocessing
                            │
                            ▼
                    Model processing
                            │
                            ▼
                     Evidence analysis
                            │
                            ▼
                 Clinical decision support
```

---

# 11. Dataset Integration Strategy

The project does **not** simply concatenate every available source into a single dataset.

Different modalities and sources have different:

* Patient populations
* Age distributions
* Labeling strategies
* Acquisition settings
* Class distributions
* Clinical contexts
* Data structures

Therefore, the project uses a **modality-specific and experiment-specific strategy**.

```text
Multiple Sources
       │
       ├── X-Ray preprocessing
       │
       ├── Laboratory preprocessing
       │
       ├── Clinical-text preprocessing
       │
       └── Structured-data preprocessing
                  │
                  ▼
           Model-specific training
                  │
                  ▼
            Evidence integration
```

This approach avoids incorrectly presenting unrelated source datasets as one directly linked patient-level cohort.

---

# 12. Dataset Size, Splits, and Class Balance

Dataset sizes reported in this repository refer to the corresponding source datasets unless explicitly identified as experiment-level samples.

### Important distinction

```text
Source Dataset Size
        ≠
Actual Experiment Sample Count
        ≠
Final Multimodal Cohort Size
```

Each experiment should therefore be interpreted together with:

* Dataset source
* Preprocessing version
* Modality
* Model branch
* Train / validation / test split
* Class distribution
* Experiment configuration

Where an exact final integrated split is not documented in the production manifest, no estimated number is reported.

This is intentional to preserve reproducibility and avoid unsupported claims.

---

# 13. Evaluation

## 13.1 X-Ray Branch Evaluation

The documented numerical results below belong to the **X-Ray Branch**.

They do **not** represent performance of the entire deployed multimodal clinical workflow.

### Validation Evaluation

Documented source-balanced validation evaluation:

* **1,958 samples**
* Accuracy: **98.21%**
* Precision: **98.46%**
* Sensitivity / Recall: **97.09%**
* Specificity: **98.97%**
* F1-score: **97.77%**
* ROC-AUC: **0.9939**

Confusion matrix:

```text
                      Predicted
                   Normal  Pneumonia

Actual Normal       1156      12
Actual Pneumonia      23     767
```

The documented experiment states that the test set was not used for training or threshold tuning.

### Test Evaluation

A separate documented source-balanced test evaluation used:

* **1,483 samples**
* Accuracy: **90.76%**
* Precision: **92.25%**
* Recall: **90.76%**
* F1-score: **91.05%**

Confusion matrix:

```text
                      Predicted
                   Normal  Pneumonia

Actual Normal        962     119
Actual Pneumonia      18     384
```

These values describe the documented X-ray experiment and should not be presented as performance of the complete multimodal system.

---

## 13.2 Clinical Fusion Evaluation

The current production clinical/vital configuration is:

```text
CLIN-NOTE   = 0.73
VITAL-FUSE  = 0.27
Threshold   = 0.665
```

A single final independently documented benchmark for the **complete deployed multimodal workflow** is not reported in this README.

This distinction is important because the architecture contains multiple evidence sources, while the currently documented numerical evaluation is primarily branch-specific.

Therefore:

> **The reported X-ray metrics represent X-ray branch performance, not end-to-end multimodal clinical performance.**

The complete integrated multimodal workflow remains an area for further benchmarking and external validation.

---

# 14. External Validation

No prospective external clinical validation study has been performed for the currently deployed system.

The documented results represent experimental model evaluation using the available datasets.

They should not be interpreted as evidence that the deployed prototype has established clinical effectiveness in routine healthcare environments.

---

# 15. Explainability

PneumoCare AI includes explainability through **Grad-CAM** for chest X-ray analysis.

The goal is to provide a visual indication of image regions associated with the model prediction.

Grad-CAM is treated as supporting evidence.

It should not be interpreted as:

* Definitive anatomical localization
* A radiological diagnosis
* Proof of causal disease localization

The system therefore presents explainability as an aid to clinical review.

---

# 16. RAG Clinical Assistant

The AI Assistant includes a retrieval-augmented generation workflow for clinical questions.

An intent-aware routing layer distinguishes between:

* **Casual** — General conversational questions
* **Patient Assessment** — Focuses on the current patient's assessment
* **X-Ray** — Focuses on the patient's chest X-ray evidence
* **Conflict** — Explains discrepancies without changing model probabilities
* **Treatment** — Focuses on treatment-support information
* **General Medical** — Provides general medical information and retrieval-supported explanations

The assistant can also detect whether the user's question is written in:

* English
* Arabic

This allows the response language to follow the actual question rather than relying only on the application's selected interface language.

---

# 17. Clinical Decision Support

The system organizes heterogeneous evidence into a clinically understandable workflow:

```text
Pneumonia Risk
      │
      ├── AI Evidence
      ├── X-Ray Evidence
      ├── Grad-CAM
      ├── Conflict Warning
      ├── Severity
      ├── Clinical Considerations
      ├── Clinical Safety
      └── Treatment Plan
```

The intended purpose is to support:

* Clinical review
* Evidence organization
* Documentation
* Explainability
* Decision support

The final clinical decision remains with a qualified healthcare professional.

---

# 18. Technology Stack

## Frontend

* React
* Vite
* Responsive web interface
* English / Arabic language support
* RTL support

## Backend

* Python 3.11
* FastAPI
* Uvicorn
* REST APIs

## Machine Learning

* PyTorch
* Torchvision
* Transformers
* ClinicalBERT
* ResNet50
* XGBoost
* Logistic Regression
* Grad-CAM

## AI Assistant

* Retrieval-Augmented Generation (RAG)
* Intent routing
* Clinical reasoning
* Treatment engine
* Gemini-based clinical explanation support

---

# 19. Project Structure

```text
PneumoCare-AI/
│
├── DEPLOY_PACKAGE/
│   │
│   ├── backend/
│   │   ├── main.py
│   │   ├── assistant_api.py
│   │   ├── capguard_engine.py
│   │   ├── intent_router.py
│   │   ├── rag_service.py
│   │   ├── treatment_engine.py
│   │   └── ...
│   │
│   ├── frontend/
│   │   ├── src/
│   │   ├── dist/
│   │   └── ...
│   │
│   └── models/
│       └── ...
│
└── README.md
```

---

# 20. API

The FastAPI backend provides endpoints for:

* Health status
* Patient management
* Patient assessments
* Assessment history
* X-ray upload and processing
* Clinical evidence processing
* AI Assistant interaction
* Clinical support workflows

The frontend communicates with the FastAPI backend through the API layer.

---

# 21. Deployment

The deployable package contains:

* React frontend
* FastAPI backend
* Model assets and configuration
* Evidence-fusion configuration
* RAG support
* Clinical decision-support logic
* Treatment-support logic
* Explainability components

GitHub repository:

**PneumoCare-AI**

`https://github.com/wedadm134-netizen/PneumoCare-AI`

---

# 22. Reproducibility

The project records the main production configuration required for reproducibility, including:

* Model configuration
* Preprocessing configuration
* Fusion weights
* Decision threshold
* Backend configuration
* Assistant routing configuration
* RAG configuration

The current clinical/vital fusion configuration is:

```text
CLIN-NOTE weight  = 0.73
VITAL-FUSE weight = 0.27
Threshold         = 0.665
```

No dynamic weight search or threshold optimization is performed during normal deployment startup.

---

# 23. Safety and Limitations

PneumoCare AI is a research and clinical decision-support prototype.

Important limitations include:

* No prospective external clinical validation
* Potential performance variation across hospitals and patient populations
* Potential dataset shift across imaging devices and acquisition protocols
* Differences in pediatric age representation
* More limited adolescent data coverage compared with younger pediatric groups
* Potentially incomplete or noisy clinical and laboratory information
* Differences between synthetic and naturally occurring clinical text
* Potential mismatch between imaging and laboratory/text source populations
* AI-generated explanations may contain errors
* Treatment support must be reviewed by qualified healthcare professionals
* The system must not be used as an autonomous prescribing system
* The system must not be used as an autonomous diagnostic system

The project documentation specifically identifies limited adolescent representation, heterogeneous sources, AI bias risk, and the need for human-in-the-loop review as important considerations.

---

# 24. Literature and References

The project is grounded in research covering pediatric pneumonia, medical imaging, clinical NLP, explainable AI, multimodal learning, and clinical decision support.

## Core References

1. **Kermany, D. S. et al. (2018).** Identifying Medical Diagnoses and Treatable Diseases by Image-Based Deep Learning. *Cell.*

2. **Alsentzer, E. et al. (2019).** Publicly Available Clinical BERT Embeddings. *Proceedings of the 2nd Clinical Natural Language Processing Workshop.*

3. **Selvaraju, R. R. et al. (2017).** Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization. *ICCV.*

4. **Rajpurkar, P. et al. (2017).** CheXNet: Radiologist-Level Pneumonia Detection on Chest X-Rays with Deep Learning.

5. **Pham, H. et al. (2023).** VinDr-PCXR pediatric chest X-ray dataset.

## Multimodal and Pediatric CAP References

6. **Wang, Y., Rao, Y., Zhu, Y., Wu, J., Qiao, B., Wu, X., Tang, Q. and Xu, Z. (2025).** Multimodal-based auxiliary diagnosis for pediatric community-acquired pneumonia. *Scientific Reports, 15.*

7. **Sikindar, S., Raghavendran, C. V. and Madhavi, G. (2026).** AI-driven multimodal imaging fusion using Swin Transformers and optimized tensor fusion networks for pneumonia detection. *Scientific Reports.*

8. **Huang, S. C., Pareek, A., Zamanian, R., Banerjee, I. and Lungren, M. P. (2021).** Multimodal fusion with deep neural networks for leveraging imaging and electronic health records.

## Pediatric Clinical Guidance

9. **Bradley, J. S. et al. (2011).** The Management of Community-Acquired Pneumonia in Infants and Children. *Clinical Infectious Diseases, 53(7), e25–e76.*

10. **World Health Organization (2024).** Guidelines for the management of pneumonia and diarrhoea in children.

The accompanying academic report contains the extended literature review and additional references related to multimodal fusion, pediatric pneumonia, clinical decision support, laboratory evidence, and explainable AI. The report also explicitly identifies recent multimodal pediatric-CAP studies including Wang et al. (2025) and Sikindar et al. (2026).

---

# 25. Research Gap

The project focuses on the challenge of combining heterogeneous pediatric evidence while accounting for variability in clinical language and age.

The research gap identified in the project includes:

* Limited integrated multimodal systems specifically focused on pediatric CAP
* Limited attention to variability in pediatric clinical-note language
* Differences in clinical descriptions across developmental stages
* Separation of imaging, laboratory, and clinical-text evidence in many existing systems
* Limited integration of diagnosis support, severity information, treatment support, explainability, and evidence-conflict awareness within one workflow

The project's literature review specifically discusses lexical variation in pediatric clinical notes and the challenge of integrating heterogeneous evidence across the 0–18 age range.

PneumoCare AI addresses this gap at the prototype level by combining:

```text
Clinical NLP
     +
Structured Laboratory Evidence
     +
Vital / Patient Information
     +
Chest X-Ray AI
     +
Explainable AI
     +
Evidence Fusion
     +
RAG Clinical Assistant
     =
Multimodal Pediatric CAP Decision Support
```

---

# 26. Academic Contribution

The project combines multiple research directions into one workflow:

```text
Pediatric CAP
      +
Clinical NLP
      +
CBC / Laboratory Evidence
      +
Vital / Structured Patient Data
      +
Chest X-Ray AI
      +
Explainable AI
      +
Evidence Fusion
      +
RAG
      +
Clinical Decision Support
      =
PneumoCare AI
```

The central contribution is the integration of heterogeneous clinical evidence into a single workflow while maintaining:

* Explainability
* Conflict awareness
* Human-in-the-loop decision making
* Reproducibility
* Multilingual interaction
* Clinical safety considerations

---

# 27. Demo

A short **2–3 minute demonstration video** is recommended as the primary project walkthrough.

### Suggested Demo Workflow

```text
1. Open PneumoCare AI
        ↓
2. Create / Select a Patient
        ↓
3. Enter Clinical Information
        ↓
4. Enter Vital / CBC Data
        ↓
5. Upload Chest X-Ray
        ↓
6. Run Assessment
        ↓
7. Review Pneumonia Risk
        ↓
8. Review AI Evidence
        ↓
9. Review X-Ray + Grad-CAM
        ↓
10. Review Conflict Warning / Severity
        ↓
11. Review Clinical Considerations
        ↓
12. Review Treatment Plan
        ↓
13. Ask the AI Assistant a Patient Question
        ↓
14. Ask an X-Ray Question
```

The demo should focus on the **actual clinical workflow and user-visible outputs**, rather than exposing internal model names or implementation-specific fusion details.

---

# 28. Project Status

**Project Status: Development / Research Prototype**

The repository contains the current deployable application package and production configuration.

The current system includes:

* Patient management
* Assessment workflow
* Clinical evidence processing
* CBC / structured evidence
* Chest X-ray analysis
* Grad-CAM explainability
* Evidence-conflict awareness
* Treatment-support workflow
* RAG clinical assistant
* English / Arabic interaction
* Clinical decision-support outputs

## Future Work

Future development areas include:

* Integrated end-to-end multimodal benchmarking
* Larger and more diverse external validation
* Prospective clinical evaluation
* Additional multimodal fusion experiments
* Improved adolescent data coverage
* Expanded clinical safety analysis
* Formal usability evaluation
* More extensive expert validation of explainability outputs

---

## Final Note

PneumoCare AI is designed as a **multimodal research and clinical decision-support platform for pediatric CAP**.

Its purpose is to organize heterogeneous patient evidence, provide interpretable AI assistance, and support—not replace—professional clinical decision making.
