from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import pdfplumber
import os
from backend.gemini import j_get_guidance, ask_insurance, categorize_message, extract_text_from_pdf

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat_with_bot(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    try:
        if file and file.filename.endswith(".pdf"):
            pdf_path = f"/tmp/{file.filename}"
            with open(pdf_path, "wb") as f:
                f.write(await file.read())
            extracted_text = extract_text_from_pdf(pdf_path)
            os.remove(pdf_path)

            answer = ask_insurance(extracted_text, message)
            return {"type": "insurance", "answer": answer}

        else:
            category = categorize_message(message)
            print(f"[DEBUG] Category: {category}")

            if category == "symptom":
                result = j_get_guidance(message)
                return {"type": "symptom", "response": result}
            elif category == "insurance":
                answer = ask_insurance("", message)
                return {"type": "insurance", "answer": answer}
            else:
                return {
                    "type": "unknown",
                    "answer": "Sorry, I couldn't understand your message."
                }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"error": "An internal error occurred. Please try again later."}
