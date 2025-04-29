import email
from pathlib import Path
from email import policy
from config import OUTPUT_DIR
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from utils.text_cleaning import clean_text
import logging
import os
import re
from email.header import decode_header

def decode_email_header(header):
    """Decode email header with proper encoding"""
    if header is None:
        return ""
    decoded_parts = []
    for part, encoding in decode_header(header):
        if isinstance(part, bytes):
            try:
                decoded_parts.append(part.decode(encoding or 'utf-8', errors='replace'))
            except:
                decoded_parts.append(part.decode('utf-8', errors='replace'))
        else:
            decoded_parts.append(part)
    return ' '.join(decoded_parts)

def handle_eml(file):
    try:
        # Read the .eml file with error handling for encoding
        with open(file, 'rb') as f:
            msg = email.message_from_binary_file(f, policy=policy.default)
        
        # Extract text content
        text = ""
        
        # Add headers with error handling
        try:
            text += f"From: {decode_email_header(msg['from'])}\n"
            text += f"To: {decode_email_header(msg['to'])}\n"
            text += f"Subject: {decode_email_header(msg['subject'])}\n"
            text += f"Date: {decode_email_header(msg['date'])}\n\n"
        except Exception as e:
            logging.warning(f"Error extracting headers from {file}: {str(e)}")
        
        # Get body content with better multipart handling
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Skip attachments
                if "attachment" in content_disposition:
                    continue
                
                # Handle different content types
                if content_type == "text/plain":
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        payload = part.get_payload(decode=True)
                        if payload:
                            text += payload.decode(charset, errors='replace')
                    except Exception as e:
                        logging.warning(f"Error decoding text/plain part in {file}: {str(e)}")
                elif content_type == "text/html":
                    try:
                        charset = part.get_content_charset() or 'utf-8'
                        payload = part.get_payload(decode=True)
                        if payload:
                            html_content = payload.decode(charset, errors='replace')
                            # Simple HTML to text conversion
                            html_content = html_content.replace('<br>', '\n').replace('<br/>', '\n')
                            html_content = re.sub(r'<[^>]+>', '', html_content)
                            text += html_content
                    except Exception as e:
                        logging.warning(f"Error decoding text/html part in {file}: {str(e)}")
        else:
            try:
                charset = msg.get_content_charset() or 'utf-8'
                payload = msg.get_payload(decode=True)
                if payload:
                    text += payload.decode(charset, errors='replace')
            except Exception as e:
                logging.warning(f"Error decoding single part message in {file}: {str(e)}")
        
        # Clean text
        text = clean_text(text)
        
        # Create PDF
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        c = canvas.Canvas(str(pdf_path), pagesize=letter)
        
        # Write text to PDF with word wrap and better formatting
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
        logging.error(f"Error processing EML file {file}: {str(e)}")
        return None, f"Error: {str(e)}" 