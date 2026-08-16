from typing import Optional
import io

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from sqlalchemy import text

from app.core.database import engine


router = APIRouter(
    prefix="/api/v1/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def get_dashboard(
    category: Optional[str] = None,
    region: Optional[str] = None,
    segment: Optional[str] = None,
    priority: Optional[str] = None,
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
    # COMMON FILTERED DATASET
    # =========================================================

    base_cte = f"""
        WITH filtered_sales AS (
            SELECT
                fs.order_id,
                fs.customer_key,
                fs.sales,
                fs.quantity,
                fs.discount,
                fs.profit,

                p.category,
                p.sub_category,

                r.region,
                r.state,
                r.city,

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
        )
    """

    response = {}


    with engine.connect() as connection:

        # =====================================================
        # 1. EXECUTIVE KPIs
        # =====================================================

        kpi_query = text(
            base_cte
            + """
            SELECT
                COALESCE(SUM(sales), 0) AS revenue,
                COALESCE(SUM(profit), 0) AS profit,
                COUNT(DISTINCT order_id) AS orders,
                COALESCE(SUM(quantity), 0) AS units_sold,
                COALESCE(AVG(discount), 0) AS average_discount

            FROM filtered_sales
            """
        )

        result = connection.execute(
            kpi_query,
            params
        ).mappings().first()

        response["kpis"] = {
            "revenue": float(result["revenue"] or 0),
            "profit": float(result["profit"] or 0),
            "orders": int(result["orders"] or 0),
            "units_sold": float(result["units_sold"] or 0),
            "average_discount": float(
                result["average_discount"] or 0
            ),
        }


        # =====================================================
        # 2. CATEGORY PERFORMANCE
        # =====================================================

        category_query = text(
            base_cte
            + """
            SELECT
                category,

                COUNT(DISTINCT order_id) AS orders,

                COALESCE(SUM(quantity), 0) AS units_sold,

                COALESCE(SUM(sales), 0) AS revenue,

                COALESCE(SUM(profit), 0) AS profit,

                COALESCE(AVG(discount), 0)
                    AS average_discount,

                CASE
                    WHEN SUM(sales) = 0
                    THEN 0
                    ELSE SUM(profit) / SUM(sales)
                END AS profit_margin

            FROM filtered_sales

            GROUP BY category

            ORDER BY profit DESC
            """
        )

        result = connection.execute(
            category_query,
            params
        ).mappings().all()

        response["categories"] = [
            dict(row)
            for row in result
        ]


        # =====================================================
        # 3. SEGMENT PERFORMANCE
        # =====================================================

        segment_query = text(
            base_cte
            + """
            SELECT
                segment,

                COUNT(DISTINCT order_id)
                    AS orders,

                COUNT(DISTINCT customer_key)
                    AS customers,

                COALESCE(SUM(quantity), 0)
                    AS units_sold,

                COALESCE(SUM(sales), 0)
                    AS revenue,

                COALESCE(SUM(profit), 0)
                    AS profit,

                COALESCE(AVG(discount), 0)
                    AS average_discount,

                CASE
                    WHEN SUM(sales) = 0
                    THEN 0
                    ELSE SUM(profit) / SUM(sales)
                END AS profit_margin

            FROM filtered_sales

            GROUP BY segment

            ORDER BY profit DESC
            """
        )

        result = connection.execute(
            segment_query,
            params
        ).mappings().all()

        response["segments"] = [
            dict(row)
            for row in result
        ]


        # =====================================================
        # 4. MONTHLY PERFORMANCE
        # =====================================================

        monthly_query = text(
            base_cte
            + """
            SELECT
                year,
                month,
                quarter,

                COUNT(DISTINCT order_id)
                    AS orders,

                COUNT(DISTINCT customer_key)
                    AS customers,

                COALESCE(SUM(quantity), 0)
                    AS units_sold,

                COALESCE(SUM(sales), 0)
                    AS revenue,

                COALESCE(SUM(profit), 0)
                    AS profit,

                COALESCE(AVG(discount), 0)
                    AS average_discount,

                CASE
                    WHEN SUM(sales) = 0
                    THEN 0
                    ELSE SUM(profit) / SUM(sales)
                END AS profit_margin

            FROM filtered_sales

            GROUP BY
                year,
                month,
                quarter

            ORDER BY
                year,
                month
            """
        )

        result = connection.execute(
            monthly_query,
            params
        ).mappings().all()

        response["monthly"] = [
            dict(row)
            for row in result
        ]


        # =====================================================
        # 5. BUSINESS ALERTS
        # =====================================================

        alerts_query = text(
            base_cte
            + """
            ,
            monthly_data AS (
                SELECT
                    year,
                    month,
                    quarter,

                    SUM(sales) AS revenue,
                    SUM(profit) AS profit,
                    AVG(discount)
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
                    ) AS previous_profit

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

                CASE
                    WHEN revenue = 0
                    THEN 0
                    ELSE profit / revenue
                END AS profit_margin,

                CASE
                    WHEN previous_revenue IS NULL
                         OR previous_revenue = 0
                    THEN 0

                    ELSE
                        (
                            revenue - previous_revenue
                        )
                        / previous_revenue
                END AS revenue_growth,

                CASE
                    WHEN previous_profit IS NULL
                         OR previous_profit = 0
                    THEN 0

                    ELSE
                        (
                            profit - previous_profit
                        )
                        / ABS(previous_profit)
                END AS profit_growth,

                average_discount,

                CASE
                    WHEN previous_profit IS NOT NULL
                         AND previous_profit <> 0
                         AND (
                            profit - previous_profit
                         )
                         / ABS(previous_profit) <= -0.50
                    THEN 'CRITICAL'

                    WHEN previous_profit IS NOT NULL
                         AND previous_profit <> 0
                         AND (
                            profit - previous_profit
                         )
                         / ABS(previous_profit) <= -0.20
                    THEN 'HIGH'

                    WHEN previous_profit IS NOT NULL
                         AND previous_profit <> 0
                         AND (
                            profit - previous_profit
                         )
                         / ABS(previous_profit) <= -0.10
                    THEN 'MEDIUM'

                    ELSE 'NORMAL'
                END AS alert_level,

                CASE
                    WHEN previous_profit IS NOT NULL
                         AND previous_profit <> 0
                         AND (
                            profit - previous_profit
                         )
                         / ABS(previous_profit) <= -0.50
                    THEN 'Profit declined by 50% or more'

                    WHEN previous_profit IS NOT NULL
                         AND previous_profit <> 0
                         AND (
                            profit - previous_profit
                         )
                         / ABS(previous_profit) <= -0.20
                    THEN 'Profit declined by 20% or more'

                    WHEN previous_profit IS NOT NULL
                         AND previous_profit <> 0
                         AND (
                            profit - previous_profit
                         )
                         / ABS(previous_profit) <= -0.10
                    THEN 'Profit declined by 10% or more'

                    ELSE 'Normal performance'
                END AS alert_reason

            FROM growth_data

            WHERE previous_profit IS NOT NULL

            AND (
                profit - previous_profit
            )
            / NULLIF(ABS(previous_profit), 0) <= -0.10

            ORDER BY
                CASE
                    WHEN (profit - previous_profit) / NULLIF(ABS(previous_profit),0) <= -0.50 THEN 1
                    WHEN (profit - previous_profit) / NULLIF(ABS(previous_profit),0) <= -0.20 THEN 2
                    WHEN (profit - previous_profit) / NULLIF(ABS(previous_profit),0) <= -0.10 THEN 3
                    ELSE 4
                END,
                ABS(
                    (profit - previous_profit)
                    / NULLIF(ABS(previous_profit), 0)
                ) DESC,
                year DESC,
                month DESC

            LIMIT 5
            """
        )

        result = connection.execute(
            alerts_query,
            params
        ).mappings().all()

        response["alerts"] = [
            dict(row)
            for row in result
        ]


        # =====================================================
        # 6. ROOT CAUSE ANALYSIS
        # =====================================================

        root_cause_query = text(
            base_cte
            + """
            SELECT
                category,
                region,
                state,
                city,

                COUNT(*) AS sales_rows,

                COALESCE(SUM(sales), 0)
                    AS revenue,

                COALESCE(SUM(profit), 0)
                    AS profit,

                COALESCE(SUM(quantity), 0)
                    AS units_sold,

                COALESCE(AVG(discount), 0)
                    AS average_discount,

                CASE
                    WHEN SUM(sales) = 0
                    THEN 0
                    ELSE SUM(profit) / SUM(sales)
                END AS profit_margin

            FROM filtered_sales

            GROUP BY
                category,
                region,
                state,
                city

            HAVING SUM(profit) < 0

            ORDER BY profit ASC

            LIMIT 20
            """
        )

        result = connection.execute(
            root_cause_query,
            params
        ).mappings().all()

        response["root_causes"] = [
            dict(row)
            for row in result
        ]


        # =====================================================
        # 7. BUSINESS RECOMMENDATIONS
        # =====================================================

        recommendation_conditions = []
        recommendation_params = {}

        if category:
            recommendation_conditions.append(
                "category = :category"
            )
            recommendation_params["category"] = category

        if region:
            recommendation_conditions.append(
                "region = :region"
            )
            recommendation_params["region"] = region

        if segment:
            recommendation_conditions.append(
                """
                category IN (
                    SELECT DISTINCT p.category
                    FROM fact_sales fs
                    JOIN dim_product p
                        ON fs.product_key = p.product_key
                    JOIN dim_customer c
                        ON fs.customer_key = c.customer_key
                    WHERE c.segment = :segment
                )
                """
            )
            recommendation_params["segment"] = segment

        if priority:
            recommendation_conditions.append(
                "priority = :priority"
            )
            recommendation_params["priority"] = priority

        recommendation_where = ""

        if recommendation_conditions:
            recommendation_where = (
                "WHERE "
                + " AND ".join(
                    recommendation_conditions
                )
            )


        recommendation_query = text(
            f"""
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

            {recommendation_where}

            ORDER BY
                CASE priority
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    ELSE 4
                END,

                root_cause_score DESC

            LIMIT 20
            """
        )

        result = connection.execute(
            recommendation_query,
            recommendation_params
        ).mappings().all()

        response["recommendations"] = [
            dict(row)
            for row in result
        ]


    return response


@router.get("/export-pdf")
def export_dashboard_pdf():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = [
        Paragraph("EDIP Executive Report", styles["Heading1"]),
        Paragraph("Enterprise Decision Intelligence Platform", styles["Heading2"]),
        Paragraph("Generated from live dashboard data.", styles["BodyText"]),
    ]

    doc.build(story)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition":
            "attachment; filename=EDIP_Executive_Report.pdf"
        }
    )