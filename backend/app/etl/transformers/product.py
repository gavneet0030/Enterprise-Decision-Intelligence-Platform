import pandas as pd


def create_dim_product(df: pd.DataFrame):

    products = (
        df[
            [
                "product_id",
                "product_name",
                "category",
                "sub_category",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    products.insert(
        0,
        "product_key",
        range(1, len(products) + 1),
    )

    print(f"Products : {len(products)}")

    return products