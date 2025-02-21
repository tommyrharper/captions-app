import torch
from model import thing, Decoder

device = (
    "mps"
    if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available() else "cpu"
)

def generate_caption(image):
    if image is None:
        return "No image provided"

    checkpoint = torch.load("model.pt", map_location=device)

    bing = thing()

    model = Decoder(n_head=2, n_inner=512).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])

    if bing is not None:
        return bing

    return "Hey I am a caption my dude"
