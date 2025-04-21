from PIL import Image
import pytesseract
from config import OUTPUT_DIR

def handle_image(file):
    image = Image.open(file)
    text = pytesseract.image_to_string(image)
    pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
    image.convert("RGB").save(pdf_path)
    return pdf_path, text
