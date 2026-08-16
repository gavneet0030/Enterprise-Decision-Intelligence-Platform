import pandas as pd


def create_dim_customer(df: pd.DataFrame):

    customers = (
        df[
            [
                "customer_id",
                "customer_name",
                "segment"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    customers.insert(
        0,
        "customer_key",
        range(1, len(customers) + 1)
    )

    print(f"Customers : {len(customers)}")

    return customers