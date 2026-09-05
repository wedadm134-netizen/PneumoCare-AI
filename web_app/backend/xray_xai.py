import os
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image


class ProductionXRayGradCAM:
    """
    CAPGuard Production X-Ray Explainability.

    Uses the exact production ResNet50 feature extractor and
    X-Ray classifier already loaded by CAPGuardModelAdapter.

    Target layer:
        ResNet50.layer4

    This module does NOT retrain or modify the production model.
    """

    def __init__(self, adapter):
        self.adapter = adapter
        self.activations = None
        self.gradients = None

        # Production feature extractor is:
        # conv1 -> bn1 -> relu -> maxpool ->
        # layer1 -> layer2 -> layer3 -> layer4 -> avgpool
        #
        # Therefore layer4 is index 7.
        self.target_layer = self.adapter.xray_feature_extractor[7]

        self.forward_handle = self.target_layer.register_forward_hook(
            self._forward_hook
        )

        self.backward_handle = self.target_layer.register_full_backward_hook(
            self._backward_hook
        )

    def _forward_hook(self, module, inputs, output):
        self.activations = output.detach()

    def _backward_hook(self, module, grad_input, grad_output):
        if grad_output and grad_output[0] is not None:
            self.gradients = grad_output[0].detach()

    def close(self):
        try:
            self.forward_handle.remove()
        except Exception:
            pass

        try:
            self.backward_handle.remove()
        except Exception:
            pass

    def generate(self, image_path, output_path):
        if not image_path:
            raise ValueError("image_path is required.")

        if not os.path.isfile(image_path):
            raise FileNotFoundError(
                f"X-Ray image not found: {image_path}"
            )

        self.activations = None
        self.gradients = None

        image = Image.open(image_path).convert("RGB")

        # EXACT production preprocessing
        x = self.adapter.xray_transform(image).unsqueeze(0)
        x = x.to(self.adapter.device)

        # Grad-CAM requires gradients.
        self.adapter.xray_feature_extractor.eval()
        self.adapter.xray_classifier.eval()

        self.adapter.xray_feature_extractor.zero_grad(set_to_none=True)
        self.adapter.xray_classifier.zero_grad(set_to_none=True)

        features_map = self.adapter.xray_feature_extractor(x)

        features = torch.flatten(
            features_map,
            1
        )

        logits = self.adapter.xray_classifier(features)

        probabilities = torch.softmax(
            logits,
            dim=1
        )[0]

        predicted_class = int(torch.argmax(probabilities).item())

        # Backpropagate the predicted class score.
        score = logits[0, predicted_class]
        score.backward()

        if self.activations is None:
            raise RuntimeError(
                "Grad-CAM activation hook did not capture layer4 output."
            )

        if self.gradients is None:
            raise RuntimeError(
                "Grad-CAM gradient hook did not capture layer4 gradients."
            )

        # Global average pooling of gradients.
        weights = self.gradients.mean(
            dim=(2, 3),
            keepdim=True
        )

        cam = (weights * self.activations).sum(
            dim=1,
            keepdim=True
        )

        cam = F.relu(cam)

        cam = F.interpolate(
            cam,
            size=(224, 224),
            mode="bilinear",
            align_corners=False
        )

        cam = cam[0, 0]

        cam_min = cam.min()
        cam_max = cam.max()

        if float(cam_max - cam_min) > 1e-8:
            cam = (
                cam - cam_min
            ) / (
                cam_max - cam_min
            )
        else:
            cam = torch.zeros_like(cam)

        heatmap = cam.detach().cpu().numpy()

        # Resize original image to production input size.
        original_resized = image.resize(
            (224, 224),
            Image.Resampling.BILINEAR
        )

        original_np = np.asarray(
            original_resized
        ).astype(np.float32)

        # Create a simple red/yellow heatmap without requiring OpenCV.
        heat = np.zeros(
            (224, 224, 3),
            dtype=np.float32
        )

        heat[:, :, 0] = heatmap
        heat[:, :, 1] = heatmap * 0.55

        # Blend original X-ray + CAM.
        alpha = 0.45

        overlay = (
            original_np * (1.0 - alpha)
            + heat * 255.0 * alpha
        )

        overlay = np.clip(
            overlay,
            0,
            255
        ).astype(np.uint8)

        overlay_image = Image.fromarray(
            overlay,
            mode="RGB"
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        overlay_image.save(
            output_path,
            format="PNG"
        )

        normal_probability = float(
            probabilities[0].detach().cpu().item()
        )

        pneumonia_probability = float(
            probabilities[1].detach().cpu().item()
        )

        return {
            "available": True,
            "model": "ResNet50 ImageNet V2",
            "target_layer": "ResNet50.layer4",
            "prediction": (
                "Pneumonia"
                if predicted_class == 1
                else "Normal"
            ),
            "normal_probability": normal_probability,
            "pneumonia_probability": pneumonia_probability,
            "image_width": 224,
            "image_height": 224,
            "explanation_type": "Grad-CAM",
            "overlay_path": str(output_path),
            "interpretation": (
                "The highlighted regions show areas that contributed "
                "to the X-Ray model prediction. Grad-CAM is an "
                "explainability aid and is not proof of disease."
            )
        }


def generate_production_gradcam(adapter, image_path, output_path):
    """
    Convenience wrapper.

    The adapter instance is reused so the production model is not
    loaded a second time.
    """
    cam = ProductionXRayGradCAM(adapter)

    try:
        return cam.generate(
            image_path=image_path,
            output_path=output_path
        )
    finally:
        cam.close()