from pathlib import Path

MAIN = Path(r"web_app\backend\main.py")

text = MAIN.read_text(encoding="utf-8")

# ------------------------------------------------------------
# Insert final decision values BEFORE XAI / Decision Explanation
# ------------------------------------------------------------

marker = """    # --------------------------------------------------------
    # X-Ray Grad-CAM Explainability
"""

insert = """    # --------------------------------------------------------
    # Final decision values
    # --------------------------------------------------------
    # These values are required by XAI and Decision Explanation.
    # They come directly from Evidence-Fuse V4.
    # --------------------------------------------------------

    final_probability = fusion_result.get(
        "pneumonia_probability"
    )

    final_prediction = fusion_result.get(
        "prediction"
    )

    if final_probability is None:
        raise HTTPException(
            status_code=500,
            detail="Evidence-Fuse V4 returned no pneumonia probability."
        )

    # --------------------------------------------------------
    # X-Ray Grad-CAM Explainability
"""

if marker not in text:
    raise RuntimeError(
        "Could not find X-Ray Grad-CAM section."
    )

if "# Final decision values" not in text:
    text = text.replace(
        marker,
        insert,
        1
    )

# ------------------------------------------------------------
# Remove the old duplicate definitions
# ------------------------------------------------------------

old_block = """    final_probability = fusion_result.get(
        "pneumonia_probability"
    )

    final_prediction = fusion_result.get(
        "prediction"
    )

"""

# Remove only the SECOND occurrence if present.
first_pos = text.find(old_block)

if first_pos != -1:
    second_pos = text.find(
        old_block,
        first_pos + len(old_block)
    )

    if second_pos != -1:
        text = (
            text[:second_pos]
            + text[second_pos + len(old_block):]
        )

MAIN.write_text(text, encoding="utf-8")

print("=" * 70)
print("CAPGuard AI — XAI ORDER FIX")
print("=" * 70)
print("UPDATED :", MAIN)
print("FIXED   : final_probability order")
print("FIXED   : final_prediction order")
print("XAI     : ENABLED")
print("FUSION  : UNCHANGED")
print("MODELS  : UNCHANGED")
print("TRAINING: NONE")
print("=" * 70)