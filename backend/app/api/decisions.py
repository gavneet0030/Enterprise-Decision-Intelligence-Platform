from typing import Optional

from fastapi import APIRouter, Query
from sqlalchemy import text

from app.core.database import engine


router = APIRouter(
    prefix="/decisions",
    tags=["Decisions"]
)


@router.get("/")
def get_decisions(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    segment: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
):
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
            root_cause_score,
            recommended_action,
            priority
        FROM vw_business_recommendations
        WHERE
            (:category IS NULL OR category = :category)
            AND (:region IS NULL OR region = :region)
            AND (:segment IS NULL OR
                EXISTS (
                    SELECT 1
                    FROM dim_customer c
                    JOIN fact_sales f
                        ON f.customer_key = c.customer_key
                    JOIN dim_product p
                        ON f.product_key = p.product_key
                    JOIN dim_region r
                        ON f.region_key = r.region_key
                    WHERE
                        c.segment = :segment
                        AND p.category = vw_business_recommendations.category
                        AND r.region = vw_business_recommendations.region
                )
            )
            AND (:priority IS NULL OR priority = :priority)

        ORDER BY
            CASE priority
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
                ELSE 5
            END,
            root_cause_score DESC

        LIMIT 20
    """)

    with engine.connect() as connection:

        result = connection.execute(
            query,
            {
                "category": category,
                "region": region,
                "segment": segment,
                "priority": priority,
            }
        ).mappings().all()

    return [dict(row) for row in result]