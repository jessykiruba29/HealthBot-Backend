from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse
from utils.r_pdf_utils import extract_fields_from_pdf, fill_pdf_fields

form_router = APIRouter()

@form_router.post("/upload-form/")
async def upload_form(file: UploadFile = File(...)):
    content = await file.read()
    
    # Save temporarily
    with open("template/r_temp.pdf", "wb") as f:
        f.write(content)

    # Extract fields from PDF (you’ll define this function)
    fields = extract_fields_from_pdf("template/r_temp.pdf")

    # AI: Generate questions (mock for now)
    questions = [f"What is your {field}?" for field in fields]

    return {"questions": questions}

@form_router.post("/fill-form/")
async def fill_form(data: dict):
    filled_pdf_path = fill_pdf_fields("template/r_temp.pdf", data)
    return FileResponse(filled_pdf_path, filename="filled_form.pdf", media_type="application/pdf")
