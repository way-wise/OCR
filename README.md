# OCR Document Processing System

A robust document processing system that handles various file formats including PDFs, images, emails, and office documents. The system extracts text content and converts documents to searchable PDFs.

## Features

- **Multi-format Support**: Processes various document types:

  - PDF files
  - Images (PNG, JPG, TIFF, BMP, WEBP)
  - Email files (EML, MSG)
  - Office documents (DOC, DOCX, PPTX, XLSX)
  - Text files (TXT, RTF, JSON)
  - Media files (MP4, MP3, WAV, GIF)

- **Advanced OCR Capabilities**:

  - Automatic rotation correction
  - Image preprocessing for better OCR results
  - Support for partially OCRed documents
  - Text quality assessment

- **Email Processing**:

  - Full message body extraction
  - Attachment handling
  - Proper encoding support
  - HTML to text conversion

- **Parallel Processing**:
  - Multi-threaded document processing
  - Configurable number of workers
  - Progress tracking and logging

## Requirements

- Python 3.8+
- Tesseract OCR
- Required Python packages (install via `pip install -r requirements.txt`):
  - pytesseract
  - opencv-python
  - pandas
  - python-docx
  - python-pptx
  - extract-msg
  - ocrmypdf
  - reportlab
  - beautifulsoup4
  - pywin32
  - pydub
  - SpeechRecognition

## Installation

1. Install Tesseract OCR:

   - Windows: Download from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
   - Set path in `config.py` if different from default

2. Clone the repository:

   ```bash
   git clone https://github.com/way-wise/OCR.git
   cd OCR
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Edit `config.py` to set:

- `NUM_WORKERS`: Number of parallel processing workers
- `OUTPUT_DIR`: Directory for processed files
- `TESSERACT_PATH`: Path to Tesseract OCR executable

## Usage

1. Place documents to process in the input directory
2. Run the main script:
   ```bash
   python main.py
   ```
3. Processed files will be saved in the output directory
4. Results are logged in `processing.log`

## Output

- Converted PDF files in the output directory
- CSV files containing:
  - `output_mapping.csv`: Mapping of original to converted files
  - `processing_errors.csv`: Any errors encountered during processing

## Error Handling

- Comprehensive error logging
- Retry mechanism for file operations
- Alternative save locations for permission issues
- Detailed error reporting in CSV format

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
