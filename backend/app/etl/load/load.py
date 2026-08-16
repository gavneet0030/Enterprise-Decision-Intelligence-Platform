from app.core.database import engine
from sqlalchemy import text


def load_dataframe(df, table_name):

    print(f"\nLoading {table_name}...")

    with engine.begin() as connection:

        connection.execute(
            text(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE')
        )

        df.to_sql(
            name=table_name,
            con=connection,
            if_exists="append",
            index=False, ,
        )

    print(f"✅ {table_name} loaded successfully.") 