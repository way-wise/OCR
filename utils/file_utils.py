from collections import defaultdict
from pathlib import Path
import logging

def collect_files_by_type(input_dir: Path):
    file_groups = defaultdict(list)
    
    try:
        # Ensure input_dir is a Path object
        input_dir = Path(input_dir)
        
        if not input_dir.exists():
            raise FileNotFoundError(f"Input directory not found: {input_dir}")
            
        # Log the start of file collection
        logging.info(f"Scanning directory: {input_dir}")
        
        # Collect all files (non-recursively since files are in root of input dir)
        for file in input_dir.glob("*"):
            if file.is_file():
                ext = file.suffix.lower()
                file_groups[ext].append(file)
                logging.debug(f"Found file: {file} with extension {ext}")
        
        # Log summary
        total_files = sum(len(files) for files in file_groups.values())
        logging.info(f"Found {total_files} files:")
        for ext, files in file_groups.items():
            logging.info(f"  {ext}: {len(files)} files")
            
        return file_groups
        
    except Exception as e:
        logging.error(f"Error collecting files: {str(e)}")
        raise
