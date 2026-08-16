import pandas as pd


def create_fact_sales(
    df: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
    regions: pd.DataFrame,
    ship_modes: pd.DataFrame,
    dates: pd.DataFrame,
) -> pd.DataFrame:

    fact = df.copy()

    # -----------------------------
    # Customer Lookup
    # -----------------------------
    customer_lookup = (
        customers
        .drop_duplicates(subset=["customer_id"])
        .set_index("customer_id")["customer_key"]
        .to_dict()
    )

    fact["customer_key"] = fact["customer_id"].map(customer_lookup)

    # -----------------------------
    # Product Lookup
    # -----------------------------
    product_lookup = (
        products
        .drop_duplicates(subset=["product_id"])
        .set_index("product_id")["product_key"]
        .to_dict()
    )

    fact["product_key"] = fact["product_id"].map(product_lookup)

    # -----------------------------
    # Region Lookup
    # -----------------------------
    region_lookup = {}

    for _, row in regions.iterrows():

        key = (
            row["region"],
            row["state"],
            row["city"],
            row["postal_code"],
        )

        if key not in region_lookup:
            region_lookup[key] = row["region_key"]

    fact["region_key"] = fact.apply(
        lambda x: region_lookup[
            (
                x["region"],
                x["state"],
                x["city"],
                x["postal_code"],
            )
        ],
        axis=1,
    )

    # -----------------------------
    # Ship Mode Lookup
    # -----------------------------
    ship_lookup = (
        ship_modes
        .drop_duplicates(subset=["ship_mode"])
        .set_index("ship_mode")["ship_mode_key"]
        .to_dict()
    )

    fact["ship_mode_key"] = fact["ship_mode"].map(ship_lookup)

    # -----------------------------
    # Date Lookup
    # -----------------------------
    date_lookup = (
        dates
        .drop_duplicates(subset=["date"])
        .set_index("date")["date_key"]
        .to_dict()
    )

    fact["date_key"] = fact["order_date"].map(date_lookup)

    # -----------------------------
    # Final Fact Table
    # -----------------------------
    fact = fact[
        [
            "order_id",
            "customer_key",
            "product_key",
            "region_key",
            "ship_mode_key",
            "date_key",
            "sales",
            "quantity",
            "discount",
            "profit",
        ]
    ]

    print(f"\nFact Sales Rows : {len(fact)}")

    return fact