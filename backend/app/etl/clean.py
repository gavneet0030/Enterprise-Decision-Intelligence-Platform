import pandas as pd


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:

    print("\n" + "=" * 80)
    print("DATA CLEANING")
    print("=" * 80)

    # Remove duplicate rows
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)

    print(f"Duplicates Removed : {before - after}")

    # Remove leading/trailing spaces from column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )

    # Convert dates
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])

    # Remove leading/trailing spaces from string columns
    string_columns = df.select_dtypes(include="object").columns

    for col in string_columns:
        df[col] = df[col].str.strip()

    print("Cleaning Completed Successfully")

    return df