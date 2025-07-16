import os
from dotenv import load_dotenv
from vertexai.language_models import ChatModel, InputOutputTextPair
import vertexai

load_dotenv()

# Set Google Cloud project + location from .env
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_REGION", "us-central1")  # default region

def get_gemini_response(disease: str) -> str:
    """
    Get expert farming advice for a disease using Gemini on Vertex AI.
    """
    if not disease:
        raise ValueError("Disease name is required for Gemini response.")

    try:
        # Initialize Vertex AI SDK
        vertexai.init(project=PROJECT_ID, location=LOCATION)

        # Load Gemini chat model
        chat_model = ChatModel.from_pretrained("chat-bison@001")
        chat = chat_model.start_chat()

        prompt = (
            f"A farmer has a tomato plant suffering from '{disease}'. "
            "Provide simple, farmer-friendly advice on:\n"
            "- Disease explanation\n"
            "- Low-cost treatments available locally\n"
            "- Current market price for tomatoes (if possible)\n"
            "- Relevant government schemes for help\n\n"
            "Please keep it short, clear, and rural-friendly."
        )

        response = chat.send_message(prompt)
        return response.text.strip()

    except Exception as e:
        raise RuntimeError(f"Vertex AI Gemini error: {e}")
