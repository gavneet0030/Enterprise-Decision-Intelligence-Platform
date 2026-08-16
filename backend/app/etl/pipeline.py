from app.etl.extract.extract import extract_superstore
from app.etl.validate import validate_dataset
from app.etl.clean import clean_dataset

from app.etl.transformers.customer import create_dim_customer
from app.etl.transformers.product import create_dim_product
from app.etl.transformers.region import create_dim_region
from app.etl.transformers.ship_mode import create_dim_ship_mode
from app.etl.transformers.date import create_dim_date
from app.etl.transformers.sales import create_fact_sales

from app.etl.load.load import load_dataframe


def run_pipeline():

    # 1. Extract
    df = extract_superstore()
 ी माताएँ, म्यूशरी, कैल्टो पेंस इन कैंपेन। गेम केलक, होस्नर पिच।
    # 2. Validate
    validate_dataset(df)

    # 3. Clean
    df = clean_dataset(df)

    # 4. Create dimensions
    customers = create_dim_customer(df)
    products = create_dim_product(df)
    regions = create_dim_region(df)
    ship_modes = create_dim_ship_mode(df)
    dates = create_dim_date(df)

    # 5. Create fact table
    fact_sales = create_fact_sales(
        df,
        customers,
        products,
        regions,
        ship_modes,
        dates,
    )

    # 6. Load dimensions
    load_dataframe(customers, "dim_customer")
    load_dataframe(products, "dim_product")
    load_dataframe(regions, "dim_region")
    load_dataframe(ship_modes, "dim_ship_mode")
    load_dataframe(dates, "dim_date")

    # 7. Load fact table
    load_dataframe(fact_sales, "fact_sales")

    # 8. Summary
    print("\n")
    print("=" * 80)
    print("DIMENSIONS CREATED")
    print("=" * 80)

    print(f"\nCustomers : {len(customers)}")
    print(f"Products  : {len(products)}")
    print(f"Regions   : {len(regions)}")
    print(f"Ship Modes: {len(ship_modes)}")
    print(f"Dates     : {len(dates)}")

    print("\nFact Sales Rows:", len(fact_sales))

    print("\nFact Sales Preview\n")
    print(fact_sales.head())


if __name__ == "__main__":
    run_pipeline()