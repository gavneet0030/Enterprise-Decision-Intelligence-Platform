import pandas as pd


def create_dim_region(df: pd.DataFrame):

    regions = (
        df[
            [
                "region",
                "state",
                "city",
                "postal_code",
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    regions.insert(
        0,
        "region_key",
        range(1, len(regions) + 1),
    )

    print(f"Regions : {len(regions)}")

    return regions