from fastapi import APIRouter
from app.core.database import engine
from sqlalchemy import text


router = APIRouter(
    prefix="/api/v1/filters",
    tags=["Filters"]
)


@router.get("/")
def get_filters():

    categories_query = text("""
        SELECT DISTINCT category
        FROM dim_product
        WHERE category IS NOT NULL
        ORDER BY category
    """)

    regions_query = text("""
        SELECT DISTINCT region
        FROM dim_region
        WHERE region IS NOT NULL
        ORDER BY region
    """)

    segments_query = text("""
        SELECT DISTINCT segment
        FROM dim_customer
        WHERE segment IS NOT NULL
        ORDER BY segment
    """)

    priorities_query = text("""
        SELECT priority
        FROM (
            SELECT DISTINCT priority
            FROM vw_business_recommendations
            WHERE priority IS NOT NULL
        ) AS p
        ORDER BY
            CASE priority
                WHEN 'CRITICAL' THEN 1
                WHEN 'HIGH' THEN 2
                WHEN 'MEDIUM' THEN 3
                WHEN 'LOW' THEN 4
                ELSE 5
            END
    """)

    with engine.connect() as connection:

        categories = connection.execute(
            categories_query
        ).mappings().all()

        regions = connection.execute(
            regions_query
        ).mappings().all()

        segments = connection.execute(
            segments_query
        ).mappings().all()

        priorities = connection.execute(
            priorities_query
        ).mappings().all()

    return {
        "categories": [dict(row) for row in categories],
        "regions": [dict(row) for row in regions],
        "segments": [dict(row) for row in segments],
        "priorities": [dict(row) for row in priorities],
    }