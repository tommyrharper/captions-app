from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from inference import generate_caption

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_image(file: UploadFile):
    # image = await file.read()
    caption = generate_caption()
    return {"caption": caption}


@app.get("/health")
async def health_check():
    return {"status": "ok"}
