from pathlib import Path
import os

# Get the project root directory (where config.py is located)
PROJECT_ROOT = Path(__file__).parent.absolute()

# Use absolute paths
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Create necessary directories
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Processing configuration
NUM_WORKERS = os.cpu_count() or 4  # Use CPU count or fallback to 4
