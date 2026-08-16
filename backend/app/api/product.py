from typing import Optional

from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine


router = APIRouter(
    prefix="/api/v1/product",
    tags=["Product Intelligence"]
)


@router.get("/")
def get_product_root_causes(
    category: Optional[str] = None,
    region: Optional[str] = None,
    segment: Optional[str] = None,
):

    conditions = []
    params = {}

    if category:
        conditions.append("p.category = :category")
        params["category"] = category

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
            p.sub_category,
            p.product_id,
            p.product_name,

            COUNT(*) AS sales_rows,

            SUM(fs.sales) AS revenue,

            SUM(fs.profit) AS profit,

            SUM(fs.quantity) AS units_sold,

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
            p.category,
            p.sub_category,
            p.product_id,
            p.product_name

        ORDER BY
            profit ASC

        LIMIT 50
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