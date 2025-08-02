from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
import pdfplumber
from gemini import j_get_guidance
from gemini import ask_insurance

app = FastAPI()

@app.post("/chat")
async def chat_with_bot(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    if file and file.filename.endswith(".pdf"):
        contents = await file.read()

        with open("temp.pdf", "wb") as f:
            f.write(contents)

        extracted_text = ""
        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    extracted_text += text + "\n"

        answer = ask_insurance(extracted_text, message)
        return {"type": "insurance", "answer": answer}

    else:
        # Symptoms
        result = j_get_guidance(message)
        return {"type": "symptom", "response": result}
