from PIL import Image
import pytesseract
import cv2
import numpy as np
from config import OUTPUT_DIR
from pathlib import Path
import os

# Set Tesseract path for Windows
TESSERACT_PATH = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image):
    try:
        # Convert PIL Image to cv2 format
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply adaptive thresholding
        gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # Detect and correct rotation
        coords = np.column_stack(np.where(gray > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = 90 + angle
        center = (gray.shape[1] // 2, gray.shape[0] // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        gray = cv2.warpAffine(gray, M, (gray.shape[1], gray.shape[0]), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        # Apply dilation to connect text components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
        gray = cv2.dilate(gray, kernel, iterations=1)
        
        # Convert back to PIL Image
        return Image.fromarray(gray)
    except Exception as e:
        print(f"Error in preprocessing image: {str(e)}")
        return image  # Return original image if preprocessing fails

def handle_image(file):
    try:
        # Check if Tesseract exists
        if not os.path.exists(TESSERACT_PATH):
            raise RuntimeError(f"Tesseract not found at {TESSERACT_PATH}. Please install Tesseract OCR.")
        
        # Set environment variable for Tesseract
        os.environ['TESSERACT_PATH'] = TESSERACT_PATH
        pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
        
        # Open image
        image = Image.open(file)
        
        # Convert to RGB if necessary
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        
        # Preprocess image for better OCR
        processed_image = preprocess_image(image)
        
        # Perform OCR with custom configuration for better accuracy
        custom_config = r'--oem 3 --psm 6 -l eng+equ+osd'  # Use LSTM OCR Engine Mode with automatic page segmentation and orientation detection
        text = pytesseract.image_to_string(processed_image, config=custom_config)
        
        # Clean up text
        text = clean_text(text)
        
        # Save as PDF
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        image.convert("RGB").save(pdf_path)
        
        if not text.strip():
            print(f"Warning: No text was extracted from {file}")
        
        return pdf_path, text
    except Exception as e:
        print(f"Error processing image {file}: {str(e)}")
        return None, f"Error: {str(e)}"
