import extract_msg
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from config import OUTPUT_DIR
from utils.text_cleaning import clean_text
import os

def handle_msg(file):
    try:
        msg = extract_msg.Message(str(file))
        
        # Extract main content
        text = f"From: {msg.sender}\n"
        text += f"To: {msg.to}\n"
        text += f"Subject: {msg.subject}\n"
        text += f"Date: {msg.date}\n\n"
        text += msg.body
        
        # Handle attachments
        if msg.attachments:
            text += "\n\nAttachments:\n"
            for attachment in msg.attachments:
                text += f"- {attachment.longFilename}\n"
                # Save attachment if it's a document
                if attachment.longFilename.lower().endswith(('.doc', '.docx', '.pdf', '.txt')):
                    attachment_path = OUTPUT_DIR / attachment.longFilename
                    with open(attachment_path, 'wb') as f:
                        f.write(attachment.data)
        
        # Clean text
        text = clean_text(text)
        
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
        
    except Exception as e:
        print(f"Error processing MSG file {file}: {str(e)}")
        return None, f"Error: {str(e)}"
