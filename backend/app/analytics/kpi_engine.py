from sqlalchemy import create_engine, text
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL)


def get_business_kpis():
    query = text("""
        SELECT
            sales_rows,
            total_orders,
            total_customers,
            total_revenue,
            total_profit,
            total_units,
            average_discount,
            profit_margin
        FROM vw_sales_summary;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        row = result.mappings().first()

    return dict(row)


def get_category_kpis():
    query = text("""
        SELECT
            category,
            revenue,
            profit,
            profit_margin,
            average_discount
        FROM vw_category_performance
        ORDER BY profit DESC;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        return [dict(row) for row in result.mappings()]


def get_region_kpis():
    query = text("""
        SELECT
            region,
            state,
            city,
            revenue,
            profit,
            profit_margin,
            average_discount
        FROM vw_region_performance
        ORDER BY profit DESC;
    """)

    with engine.connect() as connection:
        result = connection.execute(query)
        return [dict(row) for row in result.mappings()]


def generate_kpi_report():

    business = get_business_kpis()
    categories = get_category_kpis()
    regions = get_region_kpis()

    print("\n" + "=" * 70)
    print("EDIP KPI ENGINE")
    print("=" * 70)

    print("\nBUSINESS KPIs")
    print("-" * 70)

    print(f"Revenue         : ${business['total_revenue']:,.2f}")
    print(f"Profit          : ${business['total_profit']:,.2f}")
    print(f"Profit Margin   : {business['profit_margin'] * 100:.2f}%")
    print(f"Orders          : {business['total_orders']:,}")
    print(f"Customers       : {business['total_customers']:,}")
    print(f"Units Sold      : {business['total_units']:,}")
    print(
        f"Average Discount: {business['average_discount'] * 100:.2f}%"
    )

    print("\nBEST CATEGORY")
    print("-" * 70)

    best_category = categories[0]

    print(f"Category        : {best_category['category']}")
    print(f"Profit          : ${best_category['profit']:,.2f}")
    print(
        f"Margin          : {best_category['profit_margin'] * 100:.2f}%"
    )

    print("\nWORST CATEGORY")
    print("-" * 70)

    worst_category = categories[-1]

    print(f"Category        : {worst_category['category']}")
    print(f"Profit          : ${worst_category['profit']:,.2f}")
    print(
        f"Margin          : {worst_category['profit_margin'] * 100:.2f}%"
    )

    print("\nBEST REGION")
    print("-" * 70)

    best_region = regions[0]

    print(
        f"{best_region['city']}, "
        f"{best_region['state']}"
    )

    print(f"Profit          : ${best_region['profit']:,.2f}")

    print("\nWORST REGION")
    print("-" * 70)

    worst_region = regions[-1]

    print(
        f"{worst_region['city']}, "
        f"{worst_region['state']}"
    )

    print(f"Profit          : ${worst_region['profit']:,.2f}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    generate_kpi_report()