from utils.file_utils import collect_files_by_type
from process_pool import process_files_parallel
from config import INPUT_DIR
from utils.system_checks import check_system_dependencies
import sys
import logging

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('processing.log'),
            logging.StreamHandler()
        ]
    )
    
    # Check system dependencies
    logging.info("Checking system dependencies...")
    if not check_system_dependencies():
        logging.error("Missing required system dependencies. Please install them and try again.")
        sys.exit(1)
    
    # Collect and process files
    logging.info("Starting file processing...")
    file_groups = collect_files_by_type(INPUT_DIR)
    process_files_parallel(file_groups)

if __name__ == "__main__":
    main()
