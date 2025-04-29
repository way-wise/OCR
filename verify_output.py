import pandas as pd
from pathlib import Path
import fitz
import logging
from collections import defaultdict
import os

def is_searchable_pdf(pdf_path):
    """Check if a PDF is searchable by looking for text content"""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            if page.get_text().strip():
                return True
        return False
    except Exception as e:
        logging.error(f"Error checking PDF {pdf_path}: {str(e)}")
        return False

def verify_output():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('verification.log'),
            logging.StreamHandler()
        ]
    )

    # Paths
    output_dir = Path("OCR_Project/output")
    input_dir = Path("OCR_Project/input")
    mapping_file = output_dir / "output_mapping.csv"
    
    logging.info("Starting verification process...")
    
    # Check if mapping file exists
    if not mapping_file.exists():
        logging.error(f"Mapping file not found: {mapping_file}")
        return False
        
    # Read mapping file
    df = pd.read_csv(mapping_file)
    logging.info(f"Found {len(df)} records in mapping file")
    
    # Count original files by extension
    input_files = defaultdict(int)
    for file in input_dir.glob("*"):
        if file.is_file():
            input_files[file.suffix.lower()] += 1
    
    logging.info("\nOriginal files by extension:")
    for ext, count in input_files.items():
        logging.info(f"{ext}: {count} files")
    
    # Verify PDF outputs
    pdf_stats = {
        "total": 0,
        "searchable": 0,
        "missing": 0,
        "name_mismatch": 0
    }
    
    # Check each converted file
    for _, row in df.iterrows():
        orig_file = Path(row['original_file'])
        conv_file = Path(row['converted_file'])
        
        # Check if converted file exists
        if not conv_file.exists():
            pdf_stats["missing"] += 1
            logging.error(f"Missing converted file: {conv_file}")
            continue
            
        # Check filename matches (excluding extension)
        if orig_file.stem != conv_file.stem:
            pdf_stats["name_mismatch"] += 1
            logging.error(f"Filename mismatch: {orig_file.stem} != {conv_file.stem}")
        
        # Check if PDF is searchable
        pdf_stats["total"] += 1
        if is_searchable_pdf(conv_file):
            pdf_stats["searchable"] += 1
        
    # Log statistics
    logging.info("\nVerification Results:")
    logging.info(f"Total input files: {sum(input_files.values())}")
    logging.info(f"Total processed files: {len(df)}")
    logging.info(f"Total PDF outputs: {pdf_stats['total']}")
    logging.info(f"Searchable PDFs: {pdf_stats['searchable']}")
    logging.info(f"Missing PDFs: {pdf_stats['missing']}")
    logging.info(f"Filename mismatches: {pdf_stats['name_mismatch']}")
    
    # Check text quality in sample
    logging.info("\nChecking text quality in sample...")
    sample_size = min(5, len(df))
    sample = df.sample(n=sample_size)
    
    for _, row in sample.iterrows():
        text = row['extracted_text']
        if isinstance(text, str) and len(text) > 100:
            preview = text[:100].replace('\n', ' ').strip() + "..."
            logging.info(f"\nSample text from {row['original_file']}:")
            logging.info(preview)
    
    # Final assessment
    success = (
        pdf_stats["missing"] == 0 and
        pdf_stats["name_mismatch"] == 0 and
        pdf_stats["searchable"] == pdf_stats["total"]
    )
    
    if success:
        logging.info("\nAll requirements met successfully!")
    else:
        logging.warning("\nSome requirements not met. Please check the logs above.")
    
    return success

if __name__ == "__main__":
    verify_output() 