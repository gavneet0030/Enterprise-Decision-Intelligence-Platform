from fastapi import APIRouter
from sqlalchemy import text

from app.core.database import engine

router = APIRouter(
    prefix="/database",
    tags=["Database"]
)


@router.get("/")
def database_check():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "Connected Successfully",
            "status": "OK"
        }

    except Exception as e:
        return {
            "database": "Connection Failed",
            "error": str(e)
        }