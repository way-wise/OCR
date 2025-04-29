import email
from pathlib import Path
from email import policy
from config import OUTPUT_DIR
from reportlab.pdfgen import canvas

def handle_eml(file):
    # Read the .eml file
    with open(file, 'r', encoding='utf-8') as f:
        msg = email.message_from_file(f, policy=policy.default)

    # Extract headers
    text = f"From: {msg['from']}\n"
    text += f"To: {msg['to']}\n"
    text += f"Subject: {msg['subject']}\n"
    text += f"Date: {msg['date']}\n\n"

    # Extract the plain text body
    def get_body(message):
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    return part.get_content().strip()
        else:
            return message.get_content().strip()
        return ""

    text += get_body(msg)

    # Create PDF
    pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
    c = canvas.Canvas(str(pdf_path))

    # Write text to PDF (basic word wrapping)
    y = 800
    max_width = 80
    words = text.split()
    line = ""
    for word in words:
        if len(line + " " + word) < max_width:
            line += " " + word
        else:
            c.drawString(50, y, line.strip())
            y -= 15
            line = word
            if y < 50:
                c.showPage()
                y = 800
    if line:
        c.drawString(50, y, line.strip())

    c.save()
    return pdf_path, text
