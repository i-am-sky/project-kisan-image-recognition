import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_gemini_response(disease):
    prompt = f"""
    A tomato crop is affected by: {disease}.
    1. Explain what it is and how to cure it using affordable remedies.
    2. List common government schemes related to crop protection or subsidies.
    3. Estimate current tomato market prices in Karnataka.
    Provide the response in 3 simple paragraphs.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content