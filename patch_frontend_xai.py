from pathlib import Path

APP = Path(r"web_app\frontend\src\App.jsx")

text = APP.read_text(encoding="utf-8")

# ============================================================
# FIND ASSESSMENT RESULT FUNCTION
# ============================================================

start_marker = "// ASSESSMENT RESULT"
start = text.find(start_marker)

if start == -1:
    raise RuntimeError("Could not find ASSESSMENT RESULT section.")

function_start = text.find("function AssessmentResult(", start)

if function_start == -1:
    raise RuntimeError("Could not find AssessmentResult function.")

function_end = text.find("// ============================================================\n// PROBABILITY CARD", function_start)

if function_end == -1:
    raise RuntimeError("Could not find end of AssessmentResult function.")

# ============================================================
# NEW ASSESSMENT RESULT
# ============================================================

new_function = r'''function AssessmentResult({ result }) {
  const final = result?.result || {};
  const fusion = result?.fusion || {};
  const branches = result?.branches || {};
  const severity = result?.severity || {};
  const treatment = result?.treatment || {};
  const explanation = result?.decision_explanation || {};
  const xai = result?.xai || {};

  const isPneumonia = final.prediction === "Pneumonia";

  const pneumoniaProbability = Number(
    final.pneumonia_probability ?? fusion.pneumonia_probability ?? 0
  );

  const normalProbability = Number(
    final.normal_probability ?? 1 - pneumoniaProbability
  );

  const probabilityPercent = (value) =>
    `${(Number(value) * 100).toFixed(1)}%`;

  const clinicalProbability = Number(
    explanation?.contributors?.clinical_information?.probability ??
      branches?.clinical_nlp?.pneumonia_probability ??
      0
  );

  const vitalProbability = Number(
    explanation?.contributors?.vital_signs?.probability ??
      branches?.vital?.pneumonia_probability ??
      0
  );

  const clinicalWeight = Number(
    explanation?.contributors?.clinical_information?.weight ??
      fusion?.weights?.clinical ??
      0.73
  );

  const vitalWeight = Number(
    explanation?.contributors?.vital_signs?.weight ??
      fusion?.weights?.vital ??
      0.27
  );

  const threshold = Number(
    explanation?.threshold ?? fusion?.threshold ?? 0.665
  );

  const xrayProbability = Number(
    xai?.pneumonia_probability ??
      branches?.xray?.pneumonia_probability ??
      0
  );

  const conflictDetected = Boolean(
    explanation?.conflict_detected
  );

  const apiBase = API_BASE_URL.replace(/\/$/, "");

  const xaiUrl = xai?.url
    ? `${apiBase}${xai.url}`
    : null;

  const uploadedXrayUrl =
    result?.xray?.url ||
    result?.xray?.image_url ||
    result?.xray?.path ||
    null;

  const formatPercent = (value) =>
    `${(Number(value) * 100).toFixed(1)}%`;

  return (
    <section className="assessment-result-card">

      {/* ======================================================
          HEADER
      ====================================================== */}

      <div className="assessment-result-header">
        <span className="badge">
          <span className="status-dot"></span>
          AI Assessment Complete
        </span>

        <h3>CAPGuard AI Assessment Result</h3>

        <p>
          Integrated production assessment with explainable
          clinical, vital-sign, and chest X-ray evidence.
        </p>
      </div>

      {/* ======================================================
          OVERALL ASSESSMENT
      ====================================================== */}

      <div
        className={`final-result-panel ${
          isPneumonia ? "result-positive" : "result-negative"
        }`}
      >
        <div>
          <span className="result-label">
            OVERALL ASSESSMENT
          </span>

          <h4>{final.prediction || "Unknown"}</h4>

          <p>
            Overall Pneumonia Risk:
            <strong>
              {" "}
              {probabilityPercent(pneumoniaProbability)}
            </strong>
          </p>
        </div>

        <div className="probability-ring">
          <strong>
            {probabilityPercent(
              isPneumonia
                ? pneumoniaProbability
                : normalProbability
            )}
          </strong>

          <span>
            {isPneumonia ? "Pneumonia" : "Normal"}
          </span>
        </div>
      </div>

      {/* ======================================================
          SUMMARY PROBABILITIES
      ====================================================== */}

      <div className="probability-grid">
        <ProbabilityCard
          label="Pneumonia Risk"
          value={pneumoniaProbability}
          emphasis={isPneumonia}
        />

        <ProbabilityCard
          label="Normal Likelihood"
          value={normalProbability}
          emphasis={!isPneumonia}
        />

        <ProbabilityCard
          label="Decision Threshold"
          value={threshold}
          plainValue
        />
      </div>

      {/* ======================================================
          WHY DID CAPGUARD MAKE THIS DECISION?
      ====================================================== */}

      <div className="result-section explanation-section">

        <div className="result-section-title">
          <span>EXPLAINABLE AI</span>

          <h4>
            WHY DID CAPGuard MAKE THIS DECISION?
          </h4>
        </div>

        <div className="explanation-intro">
          <strong>
            Evidence-Fuse V4 uses clinical information and
            vital signs to calculate the overall pneumonia risk.
          </strong>

          <p>
            The chest X-ray model is displayed as independent
            evidence and is not included in the current
            Evidence-Fuse V4 calculation.
          </p>
        </div>

        <div className="contributor-grid">

          <EvidenceContributor
            title="Clinical Information"
            probability={clinicalProbability}
            weight={clinicalWeight}
            contribution={
              explanation?.contributors
                ?.clinical_information
                ?.weighted_contribution
            }
          />

          <EvidenceContributor
            title="Vital Signs"
            probability={vitalProbability}
            weight={vitalWeight}
            contribution={
              explanation?.contributors
                ?.vital_signs
                ?.weighted_contribution
            }
          />

        </div>

        <div className="calculation-card">

          <div className="calculation-header">
            <span>FUSION CALCULATION</span>

            <strong>
              {formatPercent(pneumoniaProbability)}
            </strong>
          </div>

          <div className="formula">
            {explanation?.calculation?.formula ||
              "0.73 × Clinical Information + 0.27 × Vital Signs"}
          </div>

          <div className="calculation-row">
            <span>Calculated Overall Risk</span>

            <strong>
              {formatPercent(
                explanation?.calculation
                  ?.calculated_probability ??
                  pneumoniaProbability
              )}
            </strong>
          </div>

          <div className="calculation-row">
            <span>Decision Threshold</span>

            <strong>
              {formatPercent(threshold)}
            </strong>
          </div>

          <div
            className={`calculation-status ${
              isPneumonia
                ? "calculation-positive"
                : "calculation-negative"
            }`}
          >
            {isPneumonia
              ? `Risk is at or above the ${formatPercent(
                  threshold
                )} threshold → Pneumonia`
              : `Risk is below the ${formatPercent(
                  threshold
                )} threshold → Normal`}
          </div>

        </div>
      </div>

      {/* ======================================================
          AI EVIDENCE
      ====================================================== */}

      <div className="result-section">

        <div className="result-section-title">
          <span>AI EVIDENCE</span>

          <h4>Individual Results</h4>
        </div>

        <div className="system-note">
          The overall pneumonia risk is based on the available
          clinical information and vital signs. The chest X-ray
          result is shown separately.
        </div>

        <div className="branch-grid">

          <BranchCard
            title="Chest X-Ray"
            model="Chest X-Ray Analysis"
            prediction={branches.xray?.prediction}
            probability={branches.xray?.pneumonia_probability}
            available={branches.xray?.available}
          />

          <BranchCard
            title="Clinical NLP"
            model="Clinical Information Analysis"
            prediction={branches.clinical_nlp?.prediction}
            probability={
              branches.clinical_nlp?.pneumonia_probability
            }
            available={branches.clinical_nlp?.available}
          />

          <BranchCard
            title="Vital Signs"
            model="Vital Signs Analysis"
            prediction={branches.vital?.prediction}
            probability={
              branches.vital?.pneumonia_probability
            }
            available={branches.vital?.available}
          />

        </div>
      </div>

      {/* ======================================================
          CHEST X-RAY EXPLANATION
      ====================================================== */}

      <div className="result-section xai-section">

        <div className="result-section-title">
          <span>EXPLAINABLE IMAGING</span>

          <h4>CHEST X-RAY EXPLANATION</h4>
        </div>

        <div className="xai-description">

          <div>
            <strong>
              ResNet50 Grad-CAM
            </strong>

            <p>
              The highlighted regions indicate areas that
              contributed to the X-ray model prediction.
              Grad-CAM is an explainability aid and is not
              proof of disease.
            </p>
          </div>

          <div className="xai-model-badge">
            <span>MODEL</span>
            <strong>
              {xai?.model || "ResNet50 ImageNet V2"}
            </strong>
          </div>

        </div>

        <div className="xai-evidence-card">

          <div className="xai-metric-row">

            <div>
              <span>Model Prediction</span>
              <strong>
                {xai?.prediction ||
                  branches?.xray?.prediction ||
                  "Unavailable"}
              </strong>
            </div>

            <div>
              <span>Pneumonia Likelihood</span>
              <strong>
                {probabilityPercent(xrayProbability)}
              </strong>
            </div>

            <div>
              <span>Target Layer</span>
              <strong>
                {xai?.target_layer || "ResNet50.layer4"}
              </strong>
            </div>

          </div>

          {xaiUrl ? (
            <div className="xai-image-grid">

              {uploadedXrayUrl ? (
                <div className="xai-image-card">
                  <div className="xai-image-label">
                    ORIGINAL CHEST X-RAY
                  </div>

                  <div className="xai-image-frame">
                    <img
                      src={uploadedXrayUrl}
                      alt="Original chest X-ray"
                    />
                  </div>
                </div>
              ) : (
                <div className="xai-image-card">
                  <div className="xai-image-label">
                    ORIGINAL CHEST X-RAY
                  </div>

                  <div className="xai-image-placeholder">
                    Original image is stored with the patient
                    assessment.
                  </div>
                </div>
              )}

              <div className="xai-image-card">
                <div className="xai-image-label">
                  GRAD-CAM EXPLANATION
                </div>

                <div className="xai-image-frame">
                  <img
                    src={xaiUrl}
                    alt="Grad-CAM chest X-ray explanation"
                  />
                </div>
              </div>

            </div>
          ) : (
            <div className="xai-unavailable">
              <strong>
                Grad-CAM unavailable for this assessment.
              </strong>

              <p>
                The X-ray assessment remains available, but an
                explanation image could not be generated.
              </p>
            </div>
          )}

        </div>

        {xai?.interpretation && (
          <div className="xai-disclaimer">
            <strong>How to interpret this image</strong>

            <p>
              {xai.interpretation}
            </p>
          </div>
        )}

      </div>

      {/* ======================================================
          CONFLICTING EVIDENCE
      ====================================================== */}

      {conflictDetected && (
        <div className="conflict-banner">

          <div className="conflict-icon">!</div>

          <div>
            <strong>
              CONFLICTING EVIDENCE
            </strong>

            <p>
              The chest X-ray model and the overall
              Evidence-Fuse V4 result do not agree.
              This discrepancy should be reviewed by a
              qualified clinician.
            </p>

            <span>
              {explanation?.interpretation ||
                "Conflicting evidence requires clinician review."}
            </span>
          </div>

        </div>
      )}

      {/* ======================================================
          FUSION
      ====================================================== */}

      <div className="result-section">

        <div className="result-section-title">
          <span>FUSION ENGINE</span>

          <h4>Evidence-Fuse V4</h4>
        </div>

        <div className="fusion-card">

          <div>
            <span>Clinical Information Weight</span>

            <strong>
              {(clinicalWeight * 100).toFixed(0)}%
            </strong>
          </div>

          <div>
            <span>Vital Signs Weight</span>

            <strong>
              {(vitalWeight * 100).toFixed(0)}%
            </strong>
          </div>

          <div>
            <span>Overall Risk</span>

            <strong>
              {probabilityPercent(
                fusion.pneumonia_probability ??
                  pneumoniaProbability
              )}
            </strong>
          </div>

        </div>
      </div>

      {/* ======================================================
          SEVERITY
      ====================================================== */}

      <div className="result-section">

        <div className="result-section-title">
          <span>CLINICAL SAFETY</span>

          <h4>Severity Assessment</h4>
        </div>

        <div className="severity-card">

          <div className="severity-main">
            <span>Severity Level</span>

            <strong
              className={`severity-${String(
                severity.severity || "low"
              ).toLowerCase()}`}
            >
              {severity.severity || "LOW"}
            </strong>
          </div>

          <div className="severity-score">
            <span>Score</span>

            <strong>
              {severity.score ?? 0}
            </strong>
          </div>

          <div className="severity-signals">
            <span>Clinical Signals</span>

            <p>
              {severity.high_risk_flags?.length
                ? severity.high_risk_flags.join(", ")
                : severity.moderate_signals?.length
                ? severity.moderate_signals.join(", ")
                : "No high-risk signals identified by the current engine."}
            </p>
          </div>

        </div>
      </div>

      {/* ======================================================
          TREATMENT SUPPORT
      ====================================================== */}

      <div className="result-section">

        <div className="result-section-title">
          <span>DECISION SUPPORT</span>

          <h4>What You Should Consider</h4>
        </div>

        <div className="treatment-card">

          {treatment.recommendations?.map(
            (recommendation, index) => (
              <div
                className="recommendation"
                key={`${recommendation}-${index}`}
              >
                <span>
                  {String(index + 1).padStart(2, "0")}
                </span>

                <p>
                  {recommendation}
                </p>
              </div>
            )
          )}

        </div>
      </div>

      {/* ======================================================
          SAFETY
      ====================================================== */}

      <div className="safety-banner">

        <div className="safety-icon">
          !
        </div>

        <div>
          <strong>
            CLINICAL DECISION SUPPORT ONLY
          </strong>

          <p>
            CAPGuard AI is an assistive medical AI system.
            Results require clinician review and confirmation.
            The system does not provide autonomous prescriptions,
            antibiotic dosing, or independent antibiotic selection.
          </p>
        </div>

      </div>

      {/* ======================================================
          METADATA
      ====================================================== */}

      <div className="result-meta">

        <span>
          Engine:{" "}
          <strong>
            {result.engine ||
              "CAPGuard Production Engine V1"}
          </strong>
        </span>

        <span>
          Models:{" "}
          <strong>
            Chest X-Ray Analysis · Clinical Information Analysis ·
            Vital Signs Analysis
          </strong>
        </span>

      </div>

    </section>
  );
}

// ============================================================
// EVIDENCE CONTRIBUTOR
// ============================================================

function EvidenceContributor({
  title,
  probability,
  weight,
  contribution,
}) {
  const contributionValue =
    contribution !== undefined && contribution !== null
      ? Number(contribution)
      : Number(probability) * Number(weight);

  return (
    <div className="evidence-contributor">

      <div className="evidence-contributor-header">
        <span>{title}</span>

        <strong>
          {formatEvidencePercent(probability)}
        </strong>
      </div>

      <div className="evidence-bar">
        <div
          className="evidence-bar-fill"
          style={{
            width: `${Math.min(
              100,
              Math.max(0, Number(probability) * 100)
            )}%`,
          }}
        ></div>
      </div>

      <div className="evidence-contributor-footer">
        <span>
          Fusion weight
        </span>

        <strong>
          {(Number(weight) * 100).toFixed(0)}%
        </strong>
      </div>

      <div className="evidence-contributor-footer">
        <span>
          Weighted contribution
        </span>

        <strong>
          {formatEvidencePercent(contributionValue)}
        </strong>
      </div>

    </div>
  );
}

function formatEvidencePercent(value) {
  return `${(Number(value) * 100).toFixed(1)}%`;
}

'''

text = text[:function_start] + new_function + text[function_end:]

APP.write_text(text, encoding="utf-8")

print("=" * 70)
print("CAPGuard AI — FRONTEND XAI UI PATCH")
print("=" * 70)
print("UPDATED :", APP)
print("OVERALL ASSESSMENT     : ENABLED")
print("DECISION EXPLANATION   : ENABLED")
print("GRAD-CAM VIEWER        : ENABLED")
print("CONFLICT WARNING       : ENABLED")
print("FUSION FORMULA         : ENABLED")
print("BACKEND / MODELS       : UNCHANGED")
print("TRAINING               : NONE")
print("=" * 70)