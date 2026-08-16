from app.etl.extract.extract import extract_superstore
from app.etl.validate import validate_dataset
from app.etl.clean import clean_dataset


def main():

    df = extract_superstore()

    validate_dataset(df)

    df = clean_dataset(df)

    print("\n")
    print(df.head())


if __name__ == "__main__":
    main()