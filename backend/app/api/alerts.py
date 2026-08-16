from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import text
from app.core.database import engine

router = APIRouter(
    prefix="/api/v1/alerts",
    tags=["Alerts"]
)


@router.get("/")
def get_profit_alerts(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    segment: Optional[str] = Query(None),
    alert_level: Optional[str] = Query(None),
):
    query = text("""
        SELECT
            year,
            month,
            quarter,
            revenue,
            previous_revenue,
            profit,
            previous_profit,
            profit_margin,
            previous_margin,
            revenue_growth,
            profit_growth,
            margin_change,
            average_discount,
            alert_level,
            alert_reason
        FROM vw_profit_alerts
        WHERE
            alert_level <> 'NORMAL'
            AND (
                :alert_level IS NULL
                OR alert_level = :alert_level
            )
        ORDER BY
            year DESC,
            month DESC
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "category": category,
                "region": region,
                "segment": segment,
                "alert_level": alert_level,
            }
        ).mappings().all()

    return [dict(row) for row in result]