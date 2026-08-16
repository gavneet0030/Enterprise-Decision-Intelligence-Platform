from typing import Optional

from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine


router = APIRouter(
    prefix="/api/v1/category",
    tags=["Category Intelligence"]
)


@router.get("/")
def get_category_intelligence(
    region: Optional[str] = None,
    segment: Optional[str] = None,
):

    conditions = []
    params = {}

    if region:
        conditions.append("r.region = :region")
        params["region"] = region

    if segment:
        conditions.append("c.segment = :segment")
        params["segment"] = segment

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
    else:
        where_clause = ""

    query = text(
        f"""
        SELECT
            p.category,

            COUNT(*) AS sales_rows,

            COUNT(DISTINCT fs.order_id) AS orders,

            SUM(fs.quantity) AS units_sold,

            SUM(fs.sales) AS revenue,

            SUM(fs.profit) AS profit,

            AVG(fs.discount) AS average_discount,

            CASE
                WHEN SUM(fs.sales) = 0
                THEN 0
                ELSE SUM(fs.profit) / SUM(fs.sales)
            END AS profit_margin

        FROM fact_sales fs

        JOIN dim_product p
            ON fs.product_key = p.product_key

        JOIN dim_region r
            ON fs.region_key = r.region_key

        JOIN dim_customer c
            ON fs.customer_key = c.customer_key

        {where_clause}

        GROUP BY
            p.category

        ORDER BY
            profit DESC
        """
    )

    with engine.connect() as connection:

        result = connection.execute(
            query,
            params
        ).mappings().all()

        return [
            dict(row)
            for row in result
        ]