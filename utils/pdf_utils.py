import fitz
import shutil
from config import OUTPUT_DIR
import ocrmypdf
import os
import logging

# Default Tesseract installation path on Windows
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def is_searchable_pdf(path):
    """Check if PDF is searchable and assess text quality"""
    try:
        doc = fitz.open(path)
        has_text = False
        total_pages = len(doc)
        text_pages = 0
        
        for page in doc:
            text = page.get_text().strip()
            if text:
                has_text = True
                text_pages += 1
                
        # Calculate text coverage ratio
        coverage = text_pages / total_pages if total_pages > 0 else 0
        return has_text, coverage
    except Exception as e:
        logging.error(f"Error checking PDF {path}: {str(e)}")
        return False, 0

# def handle_pdf(file):
#     output_path = OUTPUT_DIR / file.with_suffix(".pdf").name
#     if is_searchable_pdf(file):
#         shutil.copy(file, output_path)
#         return output_path, extract_text_from_pdf(file)
#     else:
#         ocrmypdf.ocr(str(file), str(output_path), force_ocr=True, skip_text=True, deskew=True)
#         return output_path, extract_text_from_pdf(output_path)

def handle_pdf(file):
    output_path = OUTPUT_DIR / file.with_suffix(".pdf").name
    
    try:
        # Check if truly searchable
        has_text, coverage = is_searchable_pdf(file)
        
        if has_text and coverage > 0.8:  # If 80% or more pages have text
            text = extract_text_from_pdf(file)
            if text.strip():  # Contains real text
                shutil.copy(file, output_path)
                return output_path, text
            # Else: continue to force OCR below
        
        # Apply OCR since it was empty or not searchable
        if not os.path.exists(TESSERACT_PATH):
            raise RuntimeError(f"Tesseract not found at {TESSERACT_PATH}. Please install Tesseract OCR and verify the path.")
        
        # Set the environment variable for Tesseract
        os.environ['TESSERACT_PATH'] = TESSERACT_PATH
            
        ocrmypdf.ocr(
            str(file), 
            str(output_path), 
            force_ocr=True,  # Force OCR on all pages
            deskew=True,     # Straighten pages
            optimize=1,      # Basic optimization
            skip_text=True,  # Skip pages that already have text
            output_type='pdfa'  # Create PDF/A for better compatibility
        )
        
        # Extract text from OCRed PDF
        text = extract_text_from_pdf(output_path)
        return output_path, text
        
    except Exception as e:
        logging.error(f"Error processing PDF {file}: {str(e)}")
        return None, f"Error: {str(e)}"

def extract_text_from_pdf(path):
    try:
        doc = fitz.open(path)
        text_parts = []
        
        for page in doc:
            # Extract text with formatting
            text = page.get_text("text")
            if text.strip():
                text_parts.append(text)
        
        return "\n".join(text_parts)
    except Exception as e:
        logging.error(f"Error extracting text from PDF {path}: {str(e)}")
        return ""
