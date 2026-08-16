from typing import Optional

from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine


router = APIRouter(
    prefix="/api/v1/discount",
    tags=["Discount Intelligence"]
)


@router.get("/")
def get_discount_impact(
    category: Optional[str] = None,
    region: Optional[str] = None,
    segment: Optional[str] = None,
):

    # =========================================================
    # FILTER CONDITIONS
    # =========================================================

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


    # =========================================================
    # DISCOUNT IMPACT QUERY
    # =========================================================

    query = text(
        f"""
        WITH filtered_sales AS (

            SELECT
                fs.sales,
                fs.profit,
                fs.discount,

                p.category,
                r.region,
                c.segment

            FROM fact_sales fs

            JOIN dim_product p
                ON fs.product_key = p.product_key

            JOIN dim_region r
                ON fs.region_key = r.region_key

            JOIN dim_customer c
                ON fs.customer_key = c.customer_key

            {where_clause}
        )

        SELECT

            category,

            CASE
                WHEN discount = 0
                    THEN '0%'

                WHEN discount <= 0.10
                    THEN '0-10%'

                WHEN discount <= 0.20
                    THEN '10-20%'

                WHEN discount <= 0.30
                    THEN '20-30%'

                WHEN discount <= 0.50
                    THEN '30-50%'

                ELSE '50%+'
            END AS discount_band,

            COUNT(*) AS sales_rows,

            COALESCE(SUM(sales), 0)
                AS revenue,

            COALESCE(SUM(profit), 0)
                AS profit,

            COALESCE(AVG(discount), 0)
                AS discount,

            CASE
                WHEN SUM(sales) = 0
                THEN 0

                ELSE SUM(profit) / SUM(sales)
            END AS profit_margin

        FROM filtered_sales

        GROUP BY
            category,
            CASE
                WHEN discount = 0
                    THEN '0%'

                WHEN discount <= 0.10
                    THEN '0-10%'

                WHEN discount <= 0.20
                    THEN '10-20%'

                WHEN discount <= 0.30
                    THEN '20-30%'

                WHEN discount <= 0.50
                    THEN '30-50%'

                ELSE '50%+'
            END

        ORDER BY
            category,
            discount
        """
    )


    # =========================================================
    # EXECUTE
    # =========================================================

    with engine.connect() as connection:

        result = connection.execute(
            query,
            params
        ).mappings().all()

        return [
            dict(row)
            for row in result
        ]