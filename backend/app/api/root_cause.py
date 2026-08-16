from fastapi import APIRouter
from app.core.database import engine
from sqlalchemy import text

router = APIRouter(
    prefix="/api/v1/root-cause",
    tags=["Root Cause"]
)


@router.get("/")
def get_root_causes():

    query = text("""
        SELECT
            category,
            region,
            state,
            city,
            sales_rows,
            revenue,
            profit,
            units_sold,
            average_discount,
            profit_margin,
            root_cause_score
        FROM vw_root_cause_ranked
        ORDER BY root_cause_score DESC
        LIMIT 20
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]