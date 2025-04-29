import json
from pathlib import Path
from config import OUTPUT_DIR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import striprtf.striprtf

def handle_txt(file):
    try:
        # Read text file with appropriate encoding
        try:
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(file, 'r', encoding='latin-1') as f:
                text = f.read()
        
        # Create PDF
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        create_text_pdf(pdf_path, text, file.name)
        
        return pdf_path, text
        
    except Exception as e:
        print(f"Error processing text file {file}: {str(e)}")
        return None, f"Error: {str(e)}"

def handle_rtf(file):
    try:
        # Read RTF file
        with open(file, 'r', encoding='utf-8') as f:
            rtf_text = f.read()
        
        # Convert RTF to plain text
        text = striprtf.striprtf(rtf_text)
        
        # Create PDF
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        create_text_pdf(pdf_path, text, file.name)
        
        return pdf_path, text
        
    except Exception as e:
        print(f"Error processing RTF file {file}: {str(e)}")
        return None, f"Error: {str(e)}"

def handle_json(file):
    try:
        # Read JSON file
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert JSON to formatted text
        text = json.dumps(data, indent=2)
        
        # Create PDF
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        create_text_pdf(pdf_path, text, file.name)
        
        return pdf_path, text
        
    except Exception as e:
        print(f"Error processing JSON file {file}: {str(e)}")
        return None, f"Error: {str(e)}"

def create_text_pdf(pdf_path, text, filename):
    c = canvas.Canvas(str(pdf_path), pagesize=letter)
    y = 800
    
    # Write filename as header
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, filename)
    y -= 30
    
    # Write content
    c.setFont("Helvetica", 12)
    words = text.split()
    line = ""
    for word in words:
        if len(line + " " + word) < 80:
            line += " " + word
        else:
            c.drawString(50, y, line.strip())
            y -= 15
            line = word
            if y < 50:
                c.showPage()
                y = 800
                c.setFont("Helvetica", 12)
    if line:
        c.drawString(50, y, line.strip())
    
    c.save() 