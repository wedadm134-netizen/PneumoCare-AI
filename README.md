CAPGuard AI
===========

Dual-Evidence Clinical Fusion for Early Pediatric CAP Detection

Architecture
------------

VITAL-FUSE
Structured clinical evidence
XGBoost

CLIN-NOTE
Clinical narrative evidence
Bio_ClinicalBERT

EVIDENCE-FUSE
Weighted probability fusion

Final Fusion
------------

VITAL-FUSE weight : 0.78
CLIN-NOTE weight  : 0.22
Threshold         : 0.35

Final Test Results
------------------

Accuracy    : 90.12%
Precision   : 79.17%
CAP Recall  : 86.36%
F1          : 82.61%
Specificity : 91.53%
ROC-AUC     : 0.9183
PR-AUC      : 0.8885

Confusion Matrix
----------------

[[54, 5],
 [3, 19]]

Tagline
-------

Two Sources. One Clinical Decision.

Important
---------

The test set was used only for final evaluation.
Validation data were used for model/fusion selection.