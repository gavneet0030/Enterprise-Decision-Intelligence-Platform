from fastapi import APIRouter
from app.core.database import engine
from sqlalchemy import text

router = APIRouter(
    prefix="/api/v1/filters",
    tags=["Filters"]
)

@router.get("/")
def get_filters():
    queries = {
        "categories": """
            SELECT DISTINCT category
            FROM vw_category_performance
            ORDER BY category
        """,
        "regions": """
            SELECT DISTINCT region
            FROM vw_region_performance
            ORDER BY region
        """,
        "segments": """
            SELECT DISTINCT segment
            FROM vw_segment_performance
            ORDER BY segment
        """
    }

    response = {}

    with engine.connect() as connection:
        for name, query in queries.items():
            result = connection.execute(
                text(query)
            ).mappings().all()

            response[name] = [
                dict(row)
                for row in result
            ]

    return response