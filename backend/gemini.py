import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model=genai.GenerativeModel("gemini-1.5-flash")

def j_get_guidance(symptoms: str) -> dict:
    prompt = f"""
    A patient says: "{symptoms}"

    Based on common medical practice, suggest the most appropriate hospital department the patient should go to.
    Return the response in JSON format with fields:
    - department
    - reason
    - next_steps
    """

    response = model.generate_content(prompt)

    try:
        import json
        return json.loads(response.text)
    except Exception:
        return {
            "department": "General Medicine",
            "reason": "Unable to determine exact department",
            "next_steps": "Consult a general physician"
        }
