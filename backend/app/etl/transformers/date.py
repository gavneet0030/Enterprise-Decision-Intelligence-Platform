import pandas as pd


def create_dim_date(df: pd.DataFrame):

    dates = (
        pd.DataFrame(
            {
                "date": pd.concat(
                    [
                        df["order_date"],
                        df["ship_date"],
                    ]
                ).unique()
            }
        )
        .sort_values("date")
        .reset_index(drop=True)
    )

    dates["year"] = dates["date"].dt.year
    dates["month"] = dates["date"].dt.month
    dates["day"] = dates["date"].dt.day
    dates["quarter"] = dates["date"].dt.quarter

    dates.insert(
        0,
        "date_key",
        range(1, len(dates) + 1),
    )

    print(f"Dates : {len(dates)}")

    return dates