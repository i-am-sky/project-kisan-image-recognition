import os
import torch
from torchvision import transforms
from PIL import Image
import json

# Locate model and labels relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "tomato_model.pth")
LABEL_PATH = os.path.join(BASE_DIR, "model", "labels.json")

# Initialize model and label mapping
try:
    model = torch.load(MODEL_PATH, map_location=torch.device("cpu"))
    model.eval()
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")

try:
    with open(LABEL_PATH, "r") as f:
        label_map = json.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load labels: {e}")

# Image preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict(image_path: str) -> str:
    """
    Run disease detection on the given image file.
    Returns the disease label as a string.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(input_tensor)
            _, pred = torch.max(outputs, 1)
            label = label_map.get(str(pred.item()), "Unknown Disease")
            return label
    except Exception as e:
        raise RuntimeError(f"Prediction error: {e}")
