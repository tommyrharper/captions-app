from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import torch
from transformers import GPT2Tokenizer, CLIPProcessor, CLIPModel
from model import Decoder
from inference import generate_caption

device = (
    "mps"
    if torch.backends.mps.is_available()
    else "cuda" if torch.cuda.is_available() else "cpu"
)
clip_model = CLIPModel.from_pretrained("models/clip_model").to(device)
clip_processor = CLIPProcessor.from_pretrained("models/clip_processor")
tokenizer = GPT2Tokenizer.from_pretrained("models/gpt2_tokenizer")
model = Decoder(n_head=2, n_inner=512).to(device)
checkpoint = torch.load("model.pt", map_location=device)
model.load_state_dict(checkpoint["model_state_dict"])

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_image(file: UploadFile):
    image = await file.read()
    caption = generate_caption(
        image, clip_processor, clip_model, device, tokenizer, model
    )
    return {"caption": caption}


@app.get("/health")
async def health_check():
    return {"status": device}
