from typing import Optional
from fastapi import APIRouter, Query
from sqlalchemy import text

from app.core.database import engine

router = APIRouter(
    prefix="/api/v1/region",
    tags=["Region"]
)


@router.get("/")
def get_regions(
    category: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    segment: Optional[str] = Query(None),
):
    query = text("""
        SELECT
            r.region,
            r.state,
            r.city,
            COUNT(*) AS sales_rows,
            SUM(f.sales) AS revenue,
            SUM(f.profit) AS profit,
            SUM(f.quantity) AS units_sold,
            AVG(f.discount) AS average_discount,
            CASE
                WHEN SUM(f.sales) = 0 THEN 0
                ELSE SUM(f.profit) / SUM(f.sales)
            END AS profit_margin
        FROM fact_sales f
        JOIN dim_region r
            ON f.region_key = r.region_key
        JOIN dim_product p
            ON f.product_key = p.product_key
        JOIN dim_customer c
            ON f.customer_key = c.customer_key
        WHERE
            (:category IS NULL OR p.category = :category)
            AND (:region IS NULL OR r.region = :region)
            AND (:segment IS NULL OR c.segment = :segment)
        GROUP BY
            r.region,
            r.state,
            r.city
        ORDER BY
            profit ASC
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {
                "category": category,
                "region": region,
                "segment": segment,
            }
        ).mappings().all()

    return [dict(row) for row in result]