from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import torch

def predict_image(image_path=None, model=None, processor=None, text_inputs=None, class_names=None):
    image = Image.open(image_path).convert("RGB")
    image_input = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        image_features = model.get_image_features(**image_input)
        text_features = model.get_text_features(**text_inputs)

    image_features = image_features / image_features.norm(p=2, dim=-1, keepdim=True)
    text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
    similarities = (image_features @ text_features.T).squeeze(0)

    predicted_index = similarities.argmax().item()
    predicted_label = class_names[predicted_index]
    confidence = similarities[predicted_index].item()

    return predicted_label, confidence