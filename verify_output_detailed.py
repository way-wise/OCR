import pandas as pd
from pathlib import Path
import fitz
import logging
from collections import defaultdict
import os
import re
from utils.text_cleaning import clean_text

def get_pdf_text_quality_score(text):
    """Calculate a basic quality score for extracted text"""
    if not text:
        return 0.0
    
    # Count words that look like valid English words (at least 2 chars, no weird symbols)
    words = text.split()
    valid_word_pattern = re.compile(r'^[a-zA-Z]{2,}$')
    valid_words = sum(1 for word in words if valid_word_pattern.match(word))
    
    # Calculate ratio of valid words to total words
    return valid_words / len(words) if words else 0.0

def is_searchable_pdf(pdf_path):
    """Check if a PDF is searchable and assess text quality"""
    try:
        doc = fitz.open(pdf_path)
        text_content = []
        for page in doc:
            text = page.get_text().strip()
            if text:
                text_content.append(text)
        
        if not text_content:
            return False, 0.0
            
        # Join all text and calculate quality score
        full_text = "\n".join(text_content)
        quality_score = get_pdf_text_quality_score(full_text)
        
        return True, quality_score
        
    except Exception as e:
        logging.error(f"Error checking PDF {pdf_path}: {str(e)}")
        return False, 0.0

def verify_output_detailed():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('verification_detailed.log'),
            logging.StreamHandler()
        ]
    )

    # Paths
    output_dir = Path("OCR_Project/output")
    input_dir = Path("OCR_Project/input")
    mapping_file = output_dir / "output_mapping.csv"
    
    logging.info("Starting detailed verification process...")
    
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
    
    # Detailed PDF verification
    pdf_stats = {
        "total": 0,
        "searchable": 0,
        "high_quality": 0,  # PDFs with quality score > 0.7
        "medium_quality": 0,  # PDFs with quality score 0.4-0.7
        "low_quality": 0,  # PDFs with quality score < 0.4
        "missing": 0,
        "name_mismatch": 0
    }
    
    # Quality thresholds
    HIGH_QUALITY = 0.7
    MEDIUM_QUALITY = 0.4
    
    # Check each converted file
    low_quality_files = []
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
        
        # Check if PDF is searchable and get quality score
        pdf_stats["total"] += 1
        is_searchable, quality_score = is_searchable_pdf(conv_file)
        
        if is_searchable:
            pdf_stats["searchable"] += 1
            if quality_score >= HIGH_QUALITY:
                pdf_stats["high_quality"] += 1
            elif quality_score >= MEDIUM_QUALITY:
                pdf_stats["medium_quality"] += 1
            else:
                pdf_stats["low_quality"] += 1
                low_quality_files.append((str(conv_file), quality_score))
        
    # Log detailed statistics
    logging.info("\nDetailed Verification Results:")
    logging.info(f"Total input files: {sum(input_files.values())}")
    logging.info(f"Total processed files: {len(df)}")
    logging.info(f"Total PDF outputs: {pdf_stats['total']}")
    logging.info(f"Searchable PDFs: {pdf_stats['searchable']} ({pdf_stats['searchable']/pdf_stats['total']*100:.1f}%)")
    logging.info(f"High quality PDFs: {pdf_stats['high_quality']} ({pdf_stats['high_quality']/pdf_stats['total']*100:.1f}%)")
    logging.info(f"Medium quality PDFs: {pdf_stats['medium_quality']} ({pdf_stats['medium_quality']/pdf_stats['total']*100:.1f}%)")
    logging.info(f"Low quality PDFs: {pdf_stats['low_quality']} ({pdf_stats['low_quality']/pdf_stats['total']*100:.1f}%)")
    logging.info(f"Missing PDFs: {pdf_stats['missing']}")
    logging.info(f"Filename mismatches: {pdf_stats['name_mismatch']}")
    
    # Log low quality files
    if low_quality_files:
        logging.warning("\nLow quality PDFs that may need attention:")
        for file, score in sorted(low_quality_files, key=lambda x: x[1]):
            logging.warning(f"Quality score {score:.2f}: {file}")
    
    # Check text cleaning in sample
    logging.info("\nChecking text cleaning quality...")
    sample_size = min(5, len(df))
    sample = df.sample(n=sample_size)
    
    for _, row in sample.iterrows():
        text = row['extracted_text']
        if isinstance(text, str) and len(text) > 100:
            # Show original and cleaned text
            orig_preview = text[:100].replace('\n', ' ').strip() + "..."
            cleaned_preview = clean_text(text)[:100].replace('\n', ' ').strip() + "..."
            
            logging.info(f"\nSample from {row['original_file']}:")
            logging.info(f"Original : {orig_preview}")
            logging.info(f"Cleaned  : {cleaned_preview}")
    
    # Final assessment
    success = (
        pdf_stats["missing"] == 0 and
        pdf_stats["name_mismatch"] == 0 and
        pdf_stats["searchable"] == pdf_stats["total"] and
        pdf_stats["high_quality"] + pdf_stats["medium_quality"] >= 0.9 * pdf_stats["total"]  # At least 90% good quality
    )
    
    if success:
        logging.info("\nAll requirements met successfully!")
    else:
        logging.warning("\nSome requirements not met. Please check the logs above.")
    
    return success

if __name__ == "__main__":
    verify_output_detailed() 