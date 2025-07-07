from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
import shutil
import os

from utils.predict import predict
from utils.gemini import get_gemini_response
from utils.translate import translate_to_kannada
from utils.tts import text_to_speech_kannada

app = FastAPI()

@app.post("/full-analysis")
async def analyze_crop(file: UploadFile = File(...)):
    temp_path = "backend/api/temp.jpg"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    disease = predict(temp_path)
    gemini_text = get_gemini_response(disease)
    kannada_text = translate_to_kannada(gemini_text)
    audio_path = "backend/api/response.mp3"
    text_to_speech_kannada(kannada_text, audio_path)

    return {
        "disease": disease,
        "summary": kannada_text,
        "audio_url": "/audio"
    }

@app.get("/audio")
async def get_audio():
    return FileResponse("backend/api/response.mp3", media_type="audio/mpeg")