import torch
from PIL import Image
import io


def get_image_embedding(image, clip_processor, clip_model, device):
    # Move image inputs to same device as CLIP model
    pil_image = Image.open(io.BytesIO(image))
    image_inputs = clip_processor(images=pil_image, return_tensors="pt")
    image_inputs = {k: v.to(device) for k, v in image_inputs.items()}

    with torch.no_grad():
        return clip_model.get_image_features(pixel_values=image_inputs["pixel_values"])


def generate_caption(image, clip_processor, clip_model, device, tokenizer, model):
    if image is None:
        return "No image provided"

    image_embedding = get_image_embedding(image, clip_processor, clip_model, device)

    caption = auto_regression(image_embedding, tokenizer, model)

    return caption


def auto_regression(image_embedding, tokenizer, model, min_length=5, max_length=8):
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
