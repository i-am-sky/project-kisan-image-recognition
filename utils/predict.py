import torch
from torchvision import transforms
from PIL import Image
import json
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../model/tomato_model.pth')
LABEL_PATH = os.path.join(os.path.dirname(__file__), '../model/labels.json')

model = torch.load(MODEL_PATH, map_location=torch.device('cpu'))
model.eval()

with open(LABEL_PATH, 'r') as f:
    label_map = json.load(f)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def predict(image_path: str) -> str:
    try:
        image = Image.open(image_path).convert('RGB')
        image_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(image_tensor)
            _, predicted = torch.max(outputs, 1)
            return label_map.get(str(predicted.item()), "Unknown Disease")
    except Exception as e:
        return f"Error: {str(e)}"