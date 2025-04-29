import win32com.client
from pathlib import Path
from config import OUTPUT_DIR
import pythoncom
import os

def handle_doc(file):
    try:
        # Initialize COM in this thread
        pythoncom.CoInitialize()
        
        # Create a Word application instance
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        # Convert to PDF
        pdf_path = OUTPUT_DIR / file.with_suffix(".pdf").name
        doc = word.Documents.Open(str(file.absolute()))
        doc.SaveAs(str(pdf_path.absolute()), FileFormat=17)  # 17 represents PDF format
        
        # Extract text
        text = doc.Content.Text
        
        # Cleanup
        doc.Close()
        word.Quit()
        
        return pdf_path, text
        
    except Exception as e:
        print(f"Error processing .doc file {file}: {str(e)}")
        return None, f"Error: {str(e)}"
    finally:
        pythoncom.CoUninitialize() 