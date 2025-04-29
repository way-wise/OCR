from docx import Document
from pathlib import Path
from config import OUTPUT_DIR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def handle_docx(file):
    # Read the .docx file
    doc = Document(file)
    
    # Extract text content
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    
    # Create PDF
    pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    
    # Write text to PDF with word wrap
    y = 750  # Start from top
    words = text.split()
    line = ""
    for word in words:
        if len(line + " " + word) < 80:  # Approximate characters per line
            line += " " + word
        else:
            c.drawString(50, y, line.strip())
            y -= 15  # Line spacing
            line = word
            if y < 50:  # New page if needed
                c.showPage()
                y = 750
    if line:  # Write last line
        c.drawString(50, y, line.strip())
    
    c.save()
    return pdf_path, text 