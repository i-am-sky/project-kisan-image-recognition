import os
import shutil
import tempfile
import mimetypes
import uuid
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from utils.predict import predict
from utils.gemini import get_gemini_response
from utils.translate import translate_to_kannada
from utils.tts import text_to_speech_kannada

app = FastAPI()

# Response model for structured output
class AnalysisResponse(BaseModel):
    disease: str
    summary: str
    audio_url: str

@app.post("/full-analysis", response_model=AnalysisResponse)
async def analyze_crop(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Please upload an image."
        )

    # Save image to a temporary file
    ext = mimetypes.guess_extension(file.content_type) or ".jpg"
    tmp_image = tempfile.NamedTemporaryFile(delete=False, suffix=ext)
    with tmp_image as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Prepare audio output path
    audio_filename = f"response_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(tempfile.gettempdir(), audio_filename)

    try:
        # Predict disease
        disease = predict(tmp_image.name)

        # Get expert advice and info
        gemini_text = get_gemini_response(disease)

        # Translate to Kannada
        kannada_text = translate_to_kannada(gemini_text)

        # Convert translated text to speech MP3
        text_to_speech_kannada(kannada_text, audio_path)

        return {
            "disease": disease,
            "summary": kannada_text,
            "audio_url": f"/audio/{audio_filename}"
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Processing failed: {e}"
        )
    finally:
        # Cleanup input image file
        os.remove(tmp_image.name)

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    path = os.path.join(tempfile.gettempdir(), filename)
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Audio file not found.")
    return FileResponse(path, media_type="audio/mpeg")
