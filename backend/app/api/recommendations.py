from fastapi import APIRouter
from app.core.database import engine
from sqlalchemy import text

router = APIRouter(
    prefix="/api/v1/recommendations",
    tags=["Recommendations"]
)


@router.get("/")
def get_recommendations():

    query = text("""
        SELECT
            category,
            region,
            state,
            city,
            profit,
            profit_margin,
            average_discount,
            root_cause_score,
            priority,
            recommended_action
        FROM vw_business_recommendations
        ORDER BY
            CASE priority
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                ELSE 4
            END,
            root_cause_score DESC
        LIMIT 20
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().all()

    return [dict(row) for row in result]