from fastapi import APIRouter
from app.core.database import engine
from sqlalchemy import text

router = APIRouter(prefix="/api/v1/kpis", tags=["Analytics"])


@router.get("/")
def get_kpis():

    query = text("""
        SELECT
            SUM(revenue) AS revenue,
            SUM(profit) AS profit,
            SUM(orders) AS orders,
            SUM(units_sold) AS units_sold,
            AVG(average_discount) AS average_discount
        FROM vw_monthly_performance
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()

    return {
        "revenue": float(result["revenue"] or 0),
        "profit": float(result["profit"] or 0),
        "orders": int(result["orders"] or 0),
        "units_sold": float(result["units_sold"] or 0),
        "average_discount": float(result["average_discount"] or 0)
    }


@router.get("/categories")
def get_category_performance():

    query = text("""
        SELECT
            category,
            orders,
            units_sold,
            revenue,
            profit,
            average_discount,
            profit_margin
        FROM vw_category_performance
        ORDER BY profit DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


@router.get("/segments")
def get_segment_performance():

    query = text("""
        SELECT
            segment,
            orders,
            customers,
            units_sold,
            revenue,
            profit,
            average_discount,
            profit_margin
        FROM vw_segment_performance
        ORDER BY profit DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]


@router.get("/monthly")
def get_monthly_performance():

    query = text("""
        SELECT
            year,
            month,
            quarter,
            orders,
            customers,
            units_sold,
            revenue,
            profit,
            average_discount,
            profit_margin
        FROM vw_monthly_performance
        ORDER BY year, month
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]