from collections import defaultdict
from pathlib import Path

def collect_files_by_type(input_dir: Path):
    file_groups = defaultdict(list)
    for file in input_dir.rglob("*"):
        if file.is_file():
            file_groups[file.suffix.lower()].append(file)
    return file_groups
