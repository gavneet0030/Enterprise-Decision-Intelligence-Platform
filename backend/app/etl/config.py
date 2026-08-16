from pathlib import Path

# backend/
BACKEND_DIR = Path(__file__).resolve().parents[2]

# EDIP/
PROJECT_ROOT = BACKEND_DIR.parent

# datasets/
DATASET_DIR = PROJECT_ROOT / "datasets"

# datasets/superstore.csv
DATASET_PATH = DATASET_DIR / "superstore.csv"