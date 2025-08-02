import json
import difflib
import io
import fitz  # PyMuPDF

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from typing import Annotated

from utils.r_pdf_utils import extract_fields_from_pdf, fill_pdf_fields
from gemini import generate_questions_from_fields

form_router = APIRouter()

@form_router.post("/upload-form/")
async def upload_form(file: UploadFile = File(...)):
    content = await file.read()

    # Save uploaded PDF
    saved_path = "template/r_temp.pdf"
    with open(saved_path, "wb") as f:
        f.write(content)

    # Extract field names from the uploaded PDF
    fields = extract_fields_from_pdf(saved_path)

    # Generate natural questions for the extracted fields
    questions = generate_questions_from_fields(fields)

    return {"questions": questions}

def best_match(question_text, answer_keys):
    """Return the best matching answer key using fuzzy matching."""
    matches = difflib.get_close_matches(question_text, answer_keys, n=1, cutoff=0.4)
    return matches[0] if matches else None

@form_router.post("/fill/")
async def create_filled_pdf(
    pdf: Annotated[UploadFile, File()],
    answers: Annotated[str, Form()]
):
    # Parse answers
    answers_dict = json.loads(answers)

    # Read PDF
    input_pdf = fitz.open(stream=await pdf.read(), filetype="pdf")
    page = input_pdf[0]

    # Extract all text blocks
    blocks = page.get_text("blocks")
    for block in blocks:
        x0, y0, x1, y1, text, *_ = block
        text = text.strip()

        # Skip empty text
        if not text:
            continue

        # Use fuzzy match to find closest answer key
        matched_key = best_match(text, answers_dict.keys())
        if matched_key:
            answer = answers_dict[matched_key]
            # Insert answer slightly right to the question
            page.insert_text((x1 + 10, y0), str(answer), fontsize=10)

    # Save output
    output_path = "filled_form_output.pdf"
    input_pdf.save(output_path)
    input_pdf.close()

    return {"message": "Filled successfully", "path": output_path}


@form_router.post("/fill-f/")
async def create_filled_pdf(
    pdf: Annotated[UploadFile, File()],
    answers: Annotated[str, Form()]
):
    answers_dict = json.loads(answers)

    input_pdf = fitz.open(stream=await pdf.read(), filetype="pdf")
    page = input_pdf[0]

    blocks = page.get_text("blocks")
    for block in blocks:
        x0, y0, x1, y1, text, *_ = block
        text = text.strip()

        if not text:
            continue

        matched_key = best_match(text, answers_dict.keys())
        if matched_key:
            answer = answers_dict[matched_key]
            page.insert_text((x1 + 10, y0), str(answer), fontsize=10)

    output_path = "filled_form_output.pdf"
    input_pdf.save(output_path)
    input_pdf.close()

    # Return actual file for download
    return FileResponse(output_path, filename="filled_form.pdf", media_type="application/pdf")

