from fastapi import APIRouter
from app.core.database import engine
from sqlalchemy import text

router = APIRouter(
    prefix="/api/v1/customers",
    tags=["Customers"]
)


@router.get("/")
def get_customer_performance():

    query = text("""
        SELECT
            customer_key,
            customer_id,
            customer_name,
            segment,
            orders,
            units_purchased,
            revenue,
            profit,
            average_discount,
            profit_margin
        FROM vw_customer_performance
        ORDER BY profit DESC
        LIMIT 50
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]