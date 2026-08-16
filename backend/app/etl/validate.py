import pandas as pd


def validate_dataset(df: pd.DataFrame) -> None:
    print("\n" + "=" * 80)
    print("DATA VALIDATION REPORT")
    print("=" * 80)

    print(f"\nRows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    print("\nMissing Values")
    print("-" * 80)
    print(df.isnull().sum())

    print("\nDuplicate Rows")
    print("-" * 80)
    print(df.duplicated().sum())

    print("\nData Types")
    print("-" * 80)
    print(df.dtypes)

    print("\nValidation Completed Successfully")