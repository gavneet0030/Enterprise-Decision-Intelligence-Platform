from pathlib import Path

import pandas as pd

from app.etl.config import DATASET_PATH


def extract_superstore() -> pd.DataFrame:
    """
    Extract Superstore dataset.
    """

    if not Path(DATASET_PATH).exists():
        raise FileNotFoundError(
            f"Dataset not found:\n{DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH, encoding="latin1")

    print("=" * 80)
    print("SUPERSTORE DATASET LOADED")
    print("=" * 80)

    print(f"Rows    : {df.shape[0]}")
    print(f"Columns : {df.shape[1]}")

    return df