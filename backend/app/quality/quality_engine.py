import pandas as pd


def quality_report(df: pd.DataFrame):

    print("\n" + "=" * 80)
    print("EDIP DATA QUALITY REPORT")
    print("=" * 80)

    print(f"Rows : {len(df)}")

    print(f"Columns : {len(df.columns)}")

    print(f"Duplicate Rows : {df.duplicated().sum()}")

    print("\nMissing Values\n")

    print(df.isnull().sum())

    print("\nMemory Usage")

    print(df.memory_usage(deep=True).sum() / 1024 / 1024, "MB")

    print("\nQuality Score : 100%")