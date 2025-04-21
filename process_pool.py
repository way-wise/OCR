from concurrent.futures import ProcessPoolExecutor
import pandas as pd
from config import NUM_WORKERS
from utils.text_extraction import process_file

def process_files_parallel(file_groups):
    all_files = [f for group in file_groups.values() for f in group]
    
    records = []
    with ProcessPoolExecutor(max_workers=NUM_WORKERS) as executor:
        for result in executor.map(process_file, all_files):
            orig_name, new_path, text = result
            if new_path:
                records.append({
                    "original_file": orig_name,
                    "converted_file": new_path.name,
                    "extracted_text": text
                })

    df = pd.DataFrame(records)
    df.to_csv("output/output_mapping.csv", index=False)
