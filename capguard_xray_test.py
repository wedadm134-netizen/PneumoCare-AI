import os
import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image

PROJECT = r"C:\Users\hp\Desktop\CAPGuard-AI"
RESNET = r"C:\Users\hp\.cache\torch\hub\checkpoints\resnet50-11ad3fa6.pth"

XAI_DIR = os.path.join(
    PROJECT,
    r"final_package\XRay_Branch_V1\xai"
)

print("=" * 70)
print("CAPGuard X-Ray V1 - LIVE INFERENCE TEST")
print("=" * 70)

# --------------------------------------------------
# Find original X-Ray
# --------------------------------------------------

IMAGE = None

for root, dirs, files in os.walk(XAI_DIR):
    for f in files:
        if f.lower().endswith("_original.png"):
            IMAGE = os.path.join(root, f)
            break
    if IMAGE:
        break

if IMAGE is None:
    raise FileNotFoundError("No *_original.png image found")

print("IMAGE:")
print(IMAGE)

# --------------------------------------------------
# Find classifier checkpoint
# --------------------------------------------------

candidates = [
    os.path.join(
        PROJECT,
        r"models\XRay_Branch_V1\model\best_image_classifier.pt"
    ),
    os.path.join(
        PROJECT,
        r"final_package\XRay_Branch_V1\model\best_image_classifier.pt"
    ),
    os.path.join(
        PROJECT,
        r"final_package\XRay_Branch_V1\models\best_image_classifier.pt"
    ),
]

CLASSIFIER = None

for p in candidates:
    if os.path.isfile(p):
        CLASSIFIER = p
        break

if CLASSIFIER is None:
    raise FileNotFoundError(
        "X-Ray classifier checkpoint was not found."
    )

print("CLASSIFIER:")
print(CLASSIFIER)

print()
print("DEVICE: CPU")

# --------------------------------------------------
# 1. ResNet50 V2
# --------------------------------------------------

print()
print("[1] Loading ResNet50 ImageNet V2...")

resnet = models.resnet50(weights=None)

state = torch.load(
    RESNET,
    map_location="cpu"
)

if isinstance(state, dict) and "state_dict" in state:
    state = state["state_dict"]

state = {
    k.replace("module.", ""): v
    for k, v in state.items()
}

resnet.load_state_dict(
    state,
    strict=True
)

feature_extractor = nn.Sequential(
    *list(resnet.children())[:-1]
)

feature_extractor.eval()

print("RESNET50 V2: OK")

# --------------------------------------------------
# 2. Preprocessing
# --------------------------------------------------

print()
print("[2] Preparing image preprocessing...")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# --------------------------------------------------
# 3. Load image
# --------------------------------------------------

print()
print("[3] Loading X-Ray image...")

image = Image.open(
    IMAGE
).convert("RGB")

x = transform(image).unsqueeze(0)

print("INPUT SHAPE:", tuple(x.shape))

# --------------------------------------------------
# 4. Extract 2048 features
# --------------------------------------------------

print()
print("[4] Extracting 2048-D features...")

with torch.no_grad():

    features = feature_extractor(x)

    features = torch.flatten(
        features,
        1
    )

print("FEATURE SHAPE:", tuple(features.shape))
print("FEATURE DTYPE:", features.dtype)

if tuple(features.shape) != (1, 2048):

    raise RuntimeError(
        "Expected (1, 2048), got "
        + str(tuple(features.shape))
    )

print("2048-D FEATURE EXTRACTION: OK")

# --------------------------------------------------
# 5. Load X-Ray classifier
# --------------------------------------------------

print()
print("[5] Loading X-Ray V1 classifier...")

checkpoint = torch.load(
    CLASSIFIER,
    map_location="cpu"
)

print(
    "CHECKPOINT TYPE:",
    type(checkpoint).__name__
)

if isinstance(checkpoint, dict):

    print(
        "CHECKPOINT KEYS:",
        list(checkpoint.keys())
    )

# --------------------------------------------------
# Classifier architecture
# --------------------------------------------------

class XRayClassifier(nn.Module):

    def __init__(self):

        super().__init__()

        self.network = nn.Sequential(

            nn.Linear(2048, 512),

            nn.BatchNorm1d(512),

            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(512, 128),

            nn.BatchNorm1d(128),

            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(128, 64),

            nn.ReLU(),

            nn.Dropout(0.3),

            nn.Linear(64, 2)
        )

    def forward(self, x):

        return self.network(x)


classifier = XRayClassifier()

if (
    isinstance(checkpoint, dict)
    and "model_state_dict" in checkpoint
):

    classifier.load_state_dict(
        checkpoint["model_state_dict"],
        strict=True
    )

elif isinstance(checkpoint, dict):

    classifier.load_state_dict(
        checkpoint,
        strict=True
    )

else:

    raise RuntimeError(
        "Unsupported classifier checkpoint format."
    )

classifier.eval()

print("XRAY CLASSIFIER: OK")

# --------------------------------------------------
# 6. Prediction
# --------------------------------------------------

print()
print("[6] Running prediction...")

with torch.no_grad():

    logits = classifier(features)

    probabilities = torch.softmax(
        logits,
        dim=1
    )[0]

normal_prob = float(
    probabilities[0]
)

pneumonia_prob = float(
    probabilities[1]
)

predicted_index = int(
    torch.argmax(probabilities).item()
)

labels = {
    0: "Normal",
    1: "Pneumonia"
}

# --------------------------------------------------
# Result
# --------------------------------------------------

print()
print("=" * 70)
print("RESULT")
print("=" * 70)

print(
    "PREDICTED CLASS:",
    labels[predicted_index]
)

print(
    "NORMAL PROBABILITY:",
    round(normal_prob, 6)
)

print(
    "PNEUMONIA PROBABILITY:",
    round(pneumonia_prob, 6)
)

print("=" * 70)
print("XRAY V1 LIVE INFERENCE: SUCCESS")
print("=" * 70)