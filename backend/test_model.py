import torch
from transformers import CLIPModel

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

try:
    print("Starting model load...")
    model = CLIPModel.from_pretrained("models/clip")
    print("Model loaded from disk")
    model = model.to(device)
    print("Model moved to device")
    print("Success!")
except Exception as e:
    print(f"Error: {e}") 