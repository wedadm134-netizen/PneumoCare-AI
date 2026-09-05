from pathlib import Path

MAIN = Path(r"web_app\backend\main.py")

text = MAIN.read_text(encoding="utf-8")

# ============================================================
# 1. Insert final decision values immediately BEFORE XAI
# ============================================================

marker = """    # --------------------------------------------------------
    # X-Ray Grad-CAM Explainability
"""

insert = """    # --------------------------------------------------------
    # Final decision values
    # --------------------------------------------------------
    # Evidence-Fuse V4 is the source of the final decision.
    # These values must exist before XAI / Decision Explanation.
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
        "X-Ray Grad-CAM marker was not found."
    )

# Avoid duplicate insertion.
if "    # Final decision values" not in text:
    text = text.replace(
        marker,
        insert,
        1
    )

# ============================================================
# 2. Remove the OLD definitions after "# Final decision"
# ============================================================

old_block = """    final_probability = fusion_result.get(
        "pneumonia_probability"
    )

    final_prediction = fusion_result.get(
        "prediction"
    )
"""

# Find the "# Final decision" section specifically.
final_marker = """    # --------------------------------------------------------
    # Final decision
    # --------------------------------------------------------
"""

final_pos = text.find(final_marker)

if final_pos == -1:
    raise RuntimeError(
        "Final decision section was not found."
    )

old_pos = text.find(
    old_block,
    final_pos
)

if old_pos == -1:
    raise RuntimeError(
        "Old final_probability/final_prediction block was not found."
    )

text = (
    text[:old_pos]
    + text[old_pos + len(old_block):]
)

# ============================================================
# 3. Save
# ============================================================

MAIN.write_text(
    text,
    encoding="utf-8"
)

print("=" * 70)
print("CAPGuard AI — XAI ORDER FIX V3")
print("=" * 70)
print("UPDATED :", MAIN)
print("FINAL VALUES: MOVED BEFORE XAI")
print("OLD DEFINITIONS: REMOVED")
print("GRAD-CAM: ENABLED")
print("DECISION EXPLANATION: ENABLED")
print("FUSION: UNCHANGED")
print("MODELS: UNCHANGED")
print("TRAINING: NONE")
print("=" * 70)