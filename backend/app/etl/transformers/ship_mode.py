import pandas as pd


def create_dim_ship_mode(df: pd.DataFrame):

    ship = (
        df[
            [
                "ship_mode"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    ship.insert(
        0,
        "ship_mode_key",
        range(1, len(ship) + 1),
    )

    print(f"Ship Modes : {len(ship)}")

    return ship