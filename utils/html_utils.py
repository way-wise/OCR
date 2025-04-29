from bs4 import BeautifulSoup
from pathlib import Path
from config import OUTPUT_DIR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import chardet

def handle_html(file):
    # Detect file encoding
    with open(file, 'rb') as f:
        raw_data = f.read()
        detected = chardet.detect(raw_data)
        encoding = detected['encoding'] or 'utf-8'
    
    # Read the HTML file with detected encoding
    try:
        with open(file, 'r', encoding=encoding) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
    except UnicodeDecodeError:
        # Fallback encodings if detection fails
        for enc in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                with open(file, 'r', encoding=enc) as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                break
            except UnicodeDecodeError:
                continue
    
    # Extract text content (remove script and style elements)
    for script in soup(["script", "style"]):
        script.decompose()
    text = soup.get_text(separator='\n', strip=True)
    
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