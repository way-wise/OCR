from concurrent.futures import ProcessPoolExecutor, as_completed
import pandas as pd
from config import NUM_WORKERS, OUTPUT_DIR
from utils.text_extraction import process_file
import logging
import traceback
from pathlib import Path
import time
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('processing.log'),
        logging.StreamHandler()
    ]
)

def save_dataframe_with_retry(df, output_path, max_retries=3, wait_time=2):
    """Try to save DataFrame with retries for permission issues"""
    for attempt in range(max_retries):
        try:
            # Ensure directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Try to save the file
            df.to_csv(output_path, index=False)
            return True
        except PermissionError as e:
            if attempt < max_retries - 1:
                logging.warning(f"Permission error when saving to {output_path}. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
                continue
            else:
                logging.error(f"Failed to save after {max_retries} attempts: {str(e)}")
                # Try alternative location
                alt_path = Path(os.getcwd()) / f"backup_{output_path.name}"
                try:
                    df.to_csv(alt_path, index=False)
                    logging.info(f"Saved to alternative location: {alt_path}")
                    return True
                except Exception as e2:
                    logging.error(f"Failed to save to alternative location: {str(e2)}")
                    return False
        except Exception as e:
            logging.error(f"Unexpected error saving file: {str(e)}")
            return False

def process_files_parallel(file_groups):
    all_files = [f for group in file_groups.values() for f in group]
    total_files = len(all_files)
    logging.info(f"Starting to process {total_files} files")
    
    records = []
    errors = []
    processed_count = 0
    
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        # Submit all tasks and get future objects
        future_to_file = {executor.submit(process_file, file): file for file in all_files}
        
        # Process completed tasks as they finish
        for future in as_completed(future_to_file):
            file = future_to_file[future]
            processed_count += 1
            
            try:
                orig_name, new_path, text = future.result()
                if new_path:
                    records.append({
                        "original_file": orig_name,
                        "converted_file": str(new_path),
                        "extracted_text": text
                    })
                    logging.info(f"[{processed_count}/{total_files}] Successfully processed {orig_name}")
                else:
                    error_msg = f"Failed to process {file}: No output path returned"
                    logging.error(error_msg)
                    errors.append({"file": str(file), "error": error_msg})
            except Exception as e:
                error_msg = f"Error processing {file}: {str(e)}\n{traceback.format_exc()}"
                logging.error(error_msg)
                errors.append({"file": str(file), "error": str(e)})

    # Save successful records
    if records:
        df = pd.DataFrame(records)
        output_file = OUTPUT_DIR / "output_mapping.csv"
        if save_dataframe_with_retry(df, output_file):
            logging.info(f"Successfully saved {len(records)} records to {output_file}")
        else:
            logging.error("Failed to save output mapping file")

    # Save errors if any occurred
    if errors:
        error_df = pd.DataFrame(errors)
        error_file = OUTPUT_DIR / "processing_errors.csv"
        if save_dataframe_with_retry(error_df, error_file):
            logging.error(f"Saved {len(errors)} error records to {error_file}")
        else:
            logging.error("Failed to save error records file")

    # Log final statistics
    logging.info(f"Processing completed:")
    logging.info(f"Total files: {total_files}")
    logging.info(f"Successfully processed: {len(records)}")
    logging.info(f"Failed: {len(errors)}")
    
    return len(records), len(errors)
