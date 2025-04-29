import re
import unicodedata

def clean_text(text):
    """Clean extracted text by removing extra whitespace and normalizing characters"""
    if not text:
        return ""
    
    # Normalize unicode characters
    text = unicodedata.normalize('NFKC', text)
    
    # Replace common OCR errors
    replacements = {
        r'[|]': 'l',  # OCR often mistakes l for |
        r'[`]': "'",  # Backticks to single quotes
        r'["]': '"',  # Normalize double quotes
        r'[\u2018\u2019]': "'",  # Smart quotes to straight quotes
        r'[\u201C\u201D]': '"',  # Smart double quotes to straight quotes
        r'[\u2013\u2014]': '-',  # Various dashes to hyphen
        r'[\u2026]': '...',  # Ellipsis
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)
    
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n\s*\n', '\n', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-printable characters except newlines and basic punctuation
    allowed_chars = set(' \n.,!?;:()[]{}"\'/-')
    text = ''.join(char for char in text if char.isprintable() or char in allowed_chars)
    
    # Remove leading/trailing whitespace from each line
    text = '\n'.join(line.strip() for line in text.splitlines())
    
    # Remove empty lines at start and end
    text = text.strip()
    
    return text 