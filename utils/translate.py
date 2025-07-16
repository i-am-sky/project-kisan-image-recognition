import os
from google.cloud import translate_v2 as translate
from dotenv import load_dotenv

load_dotenv()

def translate_to_kannada(text: str) -> str:
    """
    Translate the given English text to Kannada using Google Translate API.
    """
    if not text:
        raise ValueError("Text to translate cannot be empty.")

    try:
        # Assumes GOOGLE_APPLICATION_CREDENTIALS is already set via .env
        client = translate.Client()
        result = client.translate(text, target_language='kn')
        return result['translatedText']
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")
