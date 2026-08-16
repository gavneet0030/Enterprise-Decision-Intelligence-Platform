from fastapi import APIRouter
from app.core.database import engine
from sqlalchemy import text

router = APIRouter(
    prefix="/api/v1/health",
    tags=["Health"]
)


@router.get("/database")
def database_health():

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1")).scalar()

        return {
            "status": "healthy",
            "database": "connected",
            "test": result
        }

    except Exception as e:

        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
