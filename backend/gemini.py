import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)


# Use Gemini-Pro (check if available)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

import requests

ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=AIzaSyDIwuRr_iVGARu0SdRI3bia_MEAVQ8nC4k"
import re
def generate_questions_from_fields(fields: list[str]) -> list[str]:

    prompt = (
        "I have a patient onboarding form. Generate plain, natural-sounding questions "
        "for each of the following fields. Do NOT include formatting, numbering, or extra explanations. "
        "Just return the questions, one per line:\n\n" + "\n".join(fields)
    )

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(ENDPOINT, headers=headers, json=data)
    result = response.json()

    # Extract the text content
    raw_output = result['candidates'][0]['content']['parts'][0]['text']
    lines = raw_output.strip().split("\n")

    # Clean and return only actual questions
    questions = [line.strip(" -*0123456789.").strip() for line in lines if line.strip()]
    return questions