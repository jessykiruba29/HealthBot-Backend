from pdfrw import PdfReader, PdfWriter, PageMerge
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

def extract_fields_from_pdf(path: str):
    # Mock for now. Later use actual extraction.
    return ["Name", "Date of Birth", "Address", "Phone Number"]


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
