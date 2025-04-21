from pathlib import Path

# Use relative paths from project root
INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

# Create necessary directories
INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

NUM_WORKERS = 4  # Tune based on CPU
