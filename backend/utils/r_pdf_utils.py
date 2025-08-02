import fitz
from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

import fitz  # PyMuPDF

def extract_fields_from_pdf(path: str) -> list[str]:
    doc = fitz.open(path)
    all_text = []

    for page in doc:
        text = page.get_text()
        lines = text.split("\n")
        all_text.extend(lines)

    # Optional cleanup
    cleaned = [line.strip() for line in all_text if line.strip()]
    return cleaned



def fill_pdf_fields(template_path: str, data: dict):
    output_path = "template/filled_form.pdf"

    template_pdf = PdfReader(template_path)
    
    # This assumes you manually know where to place text. For demo, hardcoded positions.
    
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Example field placement
    y = 700
    for key, value in data.items():
        can.drawString(100, y, f"{key}: {value}")
        y -= 30

    can.save()
    packet.seek(0)

    overlay_pdf = PdfReader(packet)
    for i, page in enumerate(template_pdf.pages):
        merger = PageMerge(page)
        merger.add(overlay_pdf.pages[0]).render()

    PdfWriter(output_path, trailer=template_pdf).write()

    return output_path
