import torch
from model import Decoder
from transformers import GPT2Tokenizer, CLIPProcessor, CLIPModel
from PIL import Image
import io

device = (
    "mps"
    if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available() else "cpu"
)
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = Decoder(n_head=2, n_inner=512).to(device)
checkpoint = torch.load("model.pt", map_location=device)
model.load_state_dict(checkpoint["model_state_dict"])


def get_image_embedding(image):
    # Move image inputs to same device as CLIP model
    pil_image = Image.open(io.BytesIO(image))
    image_inputs = clip_processor(images=pil_image, return_tensors="pt")
    image_inputs = {k: v.to(device) for k, v in image_inputs.items()}

    with torch.no_grad():
        return clip_model.get_image_features(
            pixel_values=image_inputs["pixel_values"]
        )


def generate_caption(image):
    if image is None:
        return "No image provided"

    image_embedding = get_image_embedding(image)

    bing = auto_regression(image_embedding)

    if bing is not None:
        return bing

    return "Hey I am a caption my dude"


def auto_regression(image_embedding, min_length=5, max_length=8):
    """Generate a caption for an image."""
    model.eval()
    with torch.no_grad():
        input_ids = torch.tensor([[tokenizer.bos_token_id]]).to(image_embedding.device)
        for i in range(max_length - 1):  # Fixed max length of 77 from training
            log_probs = model(image_embedding, input_ids)

            next_token_logits = log_probs[:, -1, :]


            # Force non-EOS tokens for first min_length tokens
            if i < min_length:
                next_token_logits[0, tokenizer.eos_token_id] = float("-inf")

            # Prevent token 785 from following token 13
            if input_ids[0, -1].item() == 13:
                next_token_logits[0, 785] = float("-inf")

            next_token = torch.argmax(next_token_logits, dim=-1)


            while next_token.item() in input_ids[0]:
                next_token_logits[0, next_token.item()] = float("-inf")
                next_token = torch.argmax(next_token_logits, dim=-1)

            # Stop if we predict the end token (after min_length)
            if next_token.item() == tokenizer.eos_token_id:
                break

            input_ids = torch.cat([input_ids, next_token.unsqueeze(0)], dim=1)

        caption = tokenizer.decode(input_ids[0], skip_special_tokens=True)

        return caption
