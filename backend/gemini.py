import google.generativeai as genai
from config import GEMINI_API_KEY
import json
import re

genai.configure(api_key="AIzaSyARMBha25mYH6-FnDdkVw_56swxPChbniQ")

model=genai.GenerativeModel("gemini-1.5-flash")

def j_get_guidance(symptoms: str) -> dict:
    prompt = f"""
You are an expert hospital triage assistant.

A patient says: "{symptoms}"

Based on medical knowledge, return a JSON object like:
{{
  "department": "<Department Name>",
  "reason": "<Brief reason>",
  "next_steps": "<Steps to take>"
}}
"""

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    print("Raw Gemini Response:\n", raw_text)  
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError as e:
            print("❌ Still failed parsing JSON:", e)

    return {
        "department": "General Medicine",
        "reason": "Unable to determine exact department",
        "next_steps": "Consult a general physician"
    }

def ask_insurance(pdf_text: str, user_question: str) -> str:
    """
    Uses Gemini to answer a question based on the provided insurance PDF text.
    """
    prompt = f"""
You are an expert in understanding insurance documents.
Here is the content of a user's insurance PDF:

----- START OF INSURANCE PDF -----
{pdf_text}
----- END OF INSURANCE PDF -----

Now answer the user's question based on this document only.

Question: "{user_question}"

Respond in a helpful, friendly way with specific details from the document.
If the document doesn't contain the answer, say so politely.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error while querying Gemini: {str(e)}"