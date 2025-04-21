import extract_msg
from reportlab.pdfgen import canvas
from config import OUTPUT_DIR

def handle_msg(file):
    msg = extract_msg.Message(str(file))
    text = msg.body
    pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
    c = canvas.Canvas(str(pdf_path))
    c.drawString(100, 800, text[:1000])  # quick write (improve as needed)
    c.save()
    return pdf_path, text
