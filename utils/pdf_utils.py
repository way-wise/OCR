import fitz
import shutil
from config import OUTPUT_DIR
import ocrmypdf
import os

# Default Tesseract installation path on Windows
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def is_searchable_pdf(path):
    doc = fitz.open(path)
    return any(page.get_text().strip() for page in doc)

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

    # Check if truly searchable
    if is_searchable_pdf(file):
        text = extract_text_from_pdf(file)
        if text.strip():  # Contains real text
            shutil.copy(file, output_path)
            return output_path, text
        # Else: continue to force OCR below

    # Apply OCR since it was empty or not searchable
    if not os.path.exists(TESSERACT_PATH):
        raise RuntimeError(f"Tesseract not found at {TESSERACT_PATH}. Please install Tesseract OCR and verify the path.")
        
    ocrmypdf.ocr(
        str(file), 
        str(output_path), 
        force_ocr=True, 
        skip_text=True, 
        deskew=True,
        tesseract_path=TESSERACT_PATH
    )
    return output_path, extract_text_from_pdf(output_path)

def extract_text_from_pdf(path):
    doc = fitz.open(path)
    return "\n".join([page.get_text() for page in doc])
