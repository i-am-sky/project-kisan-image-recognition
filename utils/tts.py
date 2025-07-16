import os
from google.cloud import texttospeech
from dotenv import load_dotenv

load_dotenv()

def text_to_speech_kannada(text: str, output_path: str) -> None:
    """
    Converts Kannada text to an MP3 audio file using Google TTS.
    
    Args:
        text (str): The Kannada text to convert.
        output_path (str): Full file path to save the resulting audio.
    """
    if not text:
        raise ValueError("Text for TTS cannot be empty.")

    try:
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=text)

        voice = texttospeech.VoiceSelectionParams(
            language_code="kn-IN",  # Kannada (India)
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        with open(output_path, "wb") as out:
            out.write(response.audio_content)

    except Exception as e:
        raise RuntimeError(f"TTS failed: {e}")
