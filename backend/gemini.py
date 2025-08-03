import google.generativeai as genai
import json
import re

genai.configure(api_key="AIzaSyARMBha25mYH6-FnDdkVw_56swxPChbniQ")

model=genai.GenerativeModel("gemini-1.5-flash")

def j_get_guidance(symptoms: str) -> dict:
    prompt = f"""
You know only medical advice.

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

def ask_insurance(extracted_text: str, user_message: str) -> str:
    prompt = f"""
You are a hospital assistant who helps patients understand their insurance documents.

Here is the content extracted from a patient's insurance PDF:

--- START OF PDF ---
{extracted_text.strip()}
--- END OF PDF ---

The patient asked: "{user_message}"

Based on the PDF and the patient's question, give a helpful, concise answer. Do not ignore the document content. Be specific.
"""
    response = model.generate_content(prompt)
    return response.text

def categorize_message(message: str) -> str:
    prompt = f"""
You are a hospital assistant.

Categorize the user's message into one of the following:
- "symptom": if they are describing any physical or mental health complaints, like pain, fever, fatigue, etc.
- "insurance": if the message is about insurance coverage, claims, billing, policy duration, or similar.

Only respond with one word: either "symptom" or "insurance". Do NOT explain.

Message:
\"\"\"{message}\"\"\"
"""
    response = model.generate_content(prompt)
    return response.text.strip().lower()

import pdfplumber

def extract_text_from_pdf(path: str) -> str:
    full_text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            full_text += page.extract_text() or ""
    return full_text.strip()