from pathlib import Path

MAIN = Path(r"web_app\backend\main.py")

text = MAIN.read_text(encoding="utf-8")

# Exact XAI section inside run_assessment
xai_marker = """    # --------------------------------------------------------
    # X-Ray Grad-CAM Explainability
"""

# Exact old final decision block
old_final_block = """    # --------------------------------------------------------
    # Final decision
    # --------------------------------------------------------

    final_probability = fusion_result.get(
        "pneumonia_probability"
    )

    final_prediction = fusion_result.get(
        "prediction"
    )
"""

# New block that must appear before XAI
new_final_values = """    # --------------------------------------------------------
    # Final decision values
    # --------------------------------------------------------
    # Evidence-Fuse V4 is the source of the final decision.
    # These values are defined before XAI because the
    # Decision Explanation uses them.
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

# ------------------------------------------------------------
# 1. Find XAI section
# ------------------------------------------------------------

xai_pos = text.find(xai_marker)

if xai_pos == -1:
    raise RuntimeError(
        "X-Ray Grad-CAM section was not found."
    )

# ------------------------------------------------------------
# 2. Find the OLD final decision block AFTER XAI
# ------------------------------------------------------------

old_pos = text.find(
    old_final_block,
    xai_pos
)

if old_pos == -1:
    raise RuntimeError(
        "Old Final decision block was not found after XAI section."
    )

# ------------------------------------------------------------
# 3. Remove old definitions
# ------------------------------------------------------------

text = (
    text[:old_pos]
    + text[old_pos + len(old_final_block):]
)

# ------------------------------------------------------------
# 4. Recalculate XAI position after modification
# ------------------------------------------------------------

xai_pos = text.find(xai_marker)

if xai_pos == -1:
    raise RuntimeError(
        "X-Ray Grad-CAM section disappeared unexpectedly."
    )

# ------------------------------------------------------------
# 5. Insert final decision values immediately BEFORE XAI
# ------------------------------------------------------------

text = (
    text[:xai_pos]
    + new_final_values
    + text[xai_pos + len(xai_marker):]
)

MAIN.write_text(
    text,
    encoding="utf-8"
)

print("=" * 70)
print("CAPGuard AI — XAI ORDER FIX V2")
print("=" * 70)
print("UPDATED :", MAIN)
print("FINAL VALUES MOVED BEFORE XAI")
print("OLD DUPLICATE REMOVED")
print("GRAD-CAM: ENABLED")
print("DECISION EXPLANATION: ENABLED")
print("FUSION: UNCHANGED")
print("MODELS: UNCHANGED")
print("TRAINING: NONE")
print("=" * 70)