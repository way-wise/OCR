from utils.file_utils import collect_files_by_type
from process_pool import process_files_parallel
from config import INPUT_DIR

def main():
    file_groups = collect_files_by_type(INPUT_DIR)
    process_files_parallel(file_groups)

if __name__ == "__main__":
    main()
