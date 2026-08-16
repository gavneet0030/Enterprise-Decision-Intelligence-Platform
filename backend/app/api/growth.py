from typing import Optional

from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine


router = APIRouter(
    prefix="/api/v1/growth",
    tags=["Growth Intelligence"]
)


@router.get("/")
def get_growth(
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
    # FILTERED SALES DATASET
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
                c.segment,

                d.year,
                d.month,
                d.quarter

            FROM fact_sales fs

            JOIN dim_product p
                ON fs.product_key = p.product_key

            JOIN dim_region r
                ON fs.region_key = r.region_key

            JOIN dim_customer c
                ON fs.customer_key = c.customer_key

            JOIN dim_date d
                ON fs.date_key = d.date_key

            {where_clause}
        ),

        monthly_data AS (

            SELECT
                year,
                month,
                quarter,

                COALESCE(SUM(sales), 0)
                    AS revenue,

                COALESCE(SUM(profit), 0)
                    AS profit,

                CASE
                    WHEN SUM(sales) = 0
                    THEN 0
                    ELSE SUM(profit) / SUM(sales)
                END AS profit_margin,

                COALESCE(AVG(discount), 0)
                    AS average_discount

            FROM filtered_sales

            GROUP BY
                year,
                month,
                quarter
        ),

        growth_data AS (

            SELECT
                *,

                LAG(revenue)
                    OVER (
                        ORDER BY year, month
                    ) AS previous_revenue,

                LAG(profit)
                    OVER (
                        ORDER BY year, month
                    ) AS previous_profit,

                LAG(profit_margin)
                    OVER (
                        ORDER BY year, month
                    ) AS previous_margin

            FROM monthly_data
        )

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

            CASE
                WHEN previous_revenue IS NULL
                     OR previous_revenue = 0
                THEN 0

                ELSE
                    (
                        revenue - previous_revenue
                    ) / previous_revenue
            END AS revenue_growth,

            CASE
                WHEN previous_profit IS NULL
                     OR previous_profit = 0
                THEN 0

                ELSE
                    (
                        profit - previous_profit
                    ) / ABS(previous_profit)
            END AS profit_growth,

            (
                profit_margin - COALESCE(previous_margin, 0)
            ) AS margin_change,

            average_discount

        FROM growth_data

        ORDER BY
            year,
            month
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