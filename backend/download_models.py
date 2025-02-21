import os
from transformers import CLIPModel, CLIPProcessor, GPT2Tokenizer

base_path = "models"
model_path = f"{base_path}/clip_model"
processor_path = f"{base_path}/clip_processor"
tokenizer_path = f"{base_path}/gpt2_tokenizer"

# Create base directory if it doesn't exist
if not os.path.exists(base_path):
    os.makedirs(base_path)

# Download and save model
if not os.path.exists(model_path):
    os.makedirs(model_path)
    print("Downloading CLIP model...")
    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    model.save_pretrained(model_path)
    print(f"Model saved to {model_path}")

# Download and save processor
if not os.path.exists(processor_path):
    os.makedirs(processor_path)
    print("Downloading CLIP processor...")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    processor.save_pretrained(processor_path)
    print(f"Processor saved to {processor_path}")

# Download and save GPT2 tokenizer
if not os.path.exists(tokenizer_path):
    os.makedirs(tokenizer_path)
    print("Downloading GPT2 tokenizer...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.save_pretrained(tokenizer_path)
    print(f"Tokenizer saved to {tokenizer_path}")

if not os.path.exists(model_path):
    print("Model already exists locally") 