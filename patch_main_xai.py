from pathlib import Path

MAIN = Path(r"web_app\backend\main.py")

text = MAIN.read_text(encoding="utf-8")

# ============================================================
# 1. Add required import: FileResponse
# ============================================================

if "from fastapi.responses import FileResponse" not in text:
    marker = "from fastapi import"
    pos = text.find(marker)

    if pos == -1:
        raise RuntimeError(
            "Could not find FastAPI imports in main.py"
        )

    line_end = text.find("\n", pos)

    text = (
        text[:line_end + 1]
        + "from fastapi.responses import FileResponse\n"
        + text[line_end + 1:]
    )


# ============================================================
# 2. Add XAI endpoint before /api/health
# ============================================================

xai_endpoint = r'''
# ============================================================
# X-RAY XAI / GRAD-CAM
# ============================================================

@app.get("/api/xai/{filename}")
def get_xai_image(filename: str):

    xai_dir = (
        Path(__file__).resolve().parent.parent.parent
        / "reports"
        / "xai"
        / "xray_gradcam_v1"
    )

    file_path = xai_dir / filename

    # Prevent path traversal.
    try:
        file_path = file_path.resolve()
        xai_dir = xai_dir.resolve()

        if xai_dir not in file_path.parents:
            raise HTTPException(
                status_code=400,
                detail="Invalid XAI file path.",
            )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid XAI file path.",
        )

    if not file_path.is_file():
        raise HTTPException(
            status_code=404,
            detail="Grad-CAM image not found.",
        )

    return FileResponse(
        path=str(file_path),
        media_type="image/png",
        filename=file_path.name,
    )


'''

if '@app.get("/api/xai/{filename}")' not in text:

    health_marker = '@app.get("/api/health")'

    if health_marker not in text:
        raise RuntimeError(
            "Could not find /api/health endpoint."
        )

    text = text.replace(
        health_marker,
        xai_endpoint + health_marker,
        1
    )


# ============================================================
# 3. Add Grad-CAM + Decision Explanation
#    BEFORE "Final decision"
# ============================================================

new_xai_logic = r'''
    # --------------------------------------------------------
    # X-Ray Grad-CAM Explainability
    # --------------------------------------------------------
    #
    # This uses the SAME production ResNet50 model already
    # loaded by CAPGuardModelAdapter.
    #
    # No retraining.
    # No model modification.
    # No fusion modification.
    #
    # Target layer:
    #     ResNet50.layer4
    # --------------------------------------------------------

    xai_result = None

    try:

        from web_app.backend.xray_xai import (
            generate_production_gradcam
        )

        import uuid

        xai_dir = (
            Path(__file__).resolve().parent.parent.parent
            / "reports"
            / "xai"
            / "xray_gradcam_v1"
        )

        xai_filename = (
            f"patient_{data.patient_id}_"
            f"{uuid.uuid4().hex[:12]}_gradcam.png"
        )

        xai_output_path = (
            xai_dir / xai_filename
        )

        xai_result = (
            generate_production_gradcam(
                adapter=MODEL_ADAPTER,
                image_path=xray_path,
                output_path=xai_output_path,
            )
        )

        # Browser-accessible API URL.
        xai_result["url"] = (
            f"/api/xai/{xai_filename}"
        )

    except Exception as exc:

        errors["xai"] = str(exc)

        xai_result = {
            "available": False,
            "explanation_type": "Grad-CAM",
            "model": "ResNet50 ImageNet V2",
            "target_layer": "ResNet50.layer4",
            "error": str(exc),
        }


    # --------------------------------------------------------
    # Decision Explanation
    # --------------------------------------------------------
    #
    # Evidence-Fuse V4:
    #
    # Clinical Information = 73%
    # Vital Signs          = 27%
    # Threshold            = 66.5%
    #
    # IMPORTANT:
    # The X-Ray branch is currently independent evidence.
    # It is NOT included in the Evidence-Fuse V4 formula.
    # --------------------------------------------------------

    try:

        clinical_probability = float(
            nlp_result.get(
                "pneumonia_probability",
                0.0,
            )
        )

        vital_probability = float(
            vital_result.get(
                "pneumonia_probability",
                0.0,
            )
        )

        xray_probability = float(
            xray_result.get(
                "pneumonia_probability",
                0.0,
            )
        )

        fusion_weights = (
            fusion_result.get(
                "weights",
                {}
            )
        )

        clinical_weight = float(
            fusion_weights.get(
                "clinical",
                0.73,
            )
        )

        vital_weight = float(
            fusion_weights.get(
                "vital",
                0.27,
            )
        )

        fusion_threshold = float(
            fusion_result.get(
                "threshold",
                0.665,
            )
        )

        calculated_probability = (
            clinical_weight
            * clinical_probability
            +
            vital_weight
            * vital_probability
        )

        xray_prediction = (
            xray_result.get(
                "prediction"
            )
        )

        conflict_detected = (
            xray_prediction is not None
            and final_prediction is not None
            and xray_prediction != final_prediction
        )

        decision_explanation = {

            "final_prediction": final_prediction,

            "overall_risk": final_probability,

            "threshold": fusion_threshold,

            "contributors": {

                "clinical_information": {
                    "probability": clinical_probability,
                    "weight": clinical_weight,
                    "weighted_contribution": (
                        clinical_probability
                        * clinical_weight
                    ),
                },

                "vital_signs": {
                    "probability": vital_probability,
                    "weight": vital_weight,
                    "weighted_contribution": (
                        vital_probability
                        * vital_weight
                    ),
                },
            },

            "calculation": {

                "formula": (
                    f"{clinical_weight:.2f} "
                    "× Clinical Information + "
                    f"{vital_weight:.2f} "
                    "× Vital Signs"
                ),

                "calculated_probability": (
                    calculated_probability
                ),

                "matches_engine_result": (
                    abs(
                        calculated_probability
                        - float(final_probability)
                    ) < 1e-6
                ),
            },

            "xray_evidence": {

                "prediction": (
                    xray_prediction
                ),

                "pneumonia_probability": (
                    xray_probability
                ),

                "included_in_fusion": False,

                "explanation": (
                    "The chest X-Ray model is "
                    "reported as independent evidence "
                    "and is not included in the current "
                    "Evidence-Fuse V4 calculation."
                ),
            },

            "conflict_detected": (
                conflict_detected
            ),

            "interpretation": (

                "Conflicting evidence detected between "
                "the chest X-Ray model and the overall "
                "Evidence-Fuse V4 result. Clinician review "
                "is recommended."

                if conflict_detected

                else

                "The available clinical and vital-sign "
                "evidence is directionally consistent "
                "with the overall Evidence-Fuse V4 result."
            ),
        }

    except Exception as exc:

        errors["decision_explanation"] = str(exc)

        decision_explanation = {
            "available": False,
            "error": str(exc),
        }


'''

if '"decision_explanation"' not in text:

    final_marker = r'''    # --------------------------------------------------------
    # Final decision
    # --------------------------------------------------------
'''

    if final_marker not in text:
        raise RuntimeError(
            "Could not find Final decision section."
        )

    text = text.replace(
        final_marker,
        new_xai_logic + "\n" + final_marker,
        1
    )


# ============================================================
# 4. Add decision_explanation + xai to response
# ============================================================

old_response = r'''        "fusion": fusion_result,

        "branches": {
'''

new_response = r'''        "fusion": fusion_result,

        "decision_explanation": decision_explanation,

        "xai": xai_result,

        "branches": {
'''

if old_response in text:

    text = text.replace(
        old_response,
        new_response,
        1
    )

elif '"decision_explanation": decision_explanation' not in text:

    raise RuntimeError(
        "Could not find response fusion section."
    )


# ============================================================
# 5. Save
# ============================================================

MAIN.write_text(
    text,
    encoding="utf-8"
)

print("=" * 70)
print("CAPGuard MAIN.PY XAI PATCH")
print("=" * 70)
print("UPDATED :", MAIN)
print("Grad-CAM: ENABLED")
print("Decision Explanation: ENABLED")
print("XAI endpoint: ENABLED")
print("Fusion weights: UNCHANGED")
print("Production models: UNCHANGED")
print("Retraining: NONE")
print("=" * 70)