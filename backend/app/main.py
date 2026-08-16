from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.db import router as database_router
from app.api.decisions import router as decisions_router
from app.api.kpi import router as kpi_router
from app.api.alerts import router as alerts_router
from app.api.root_cause import router as root_cause_router
from app.api.recommendations import router as recommendations_router
from app.api.customer import router as customer_router
from app.api.product import router as product_router
from app.api.region import router as region_router
from app.api.category import router as category_router
from app.api.discount import router as discount_router
from app.api.growth import router as growth_router
from app.api.dashboard import router as dashboard_router
from app.api.filters import router as filters_router
from app.api.export import router as export_router  # Added Export Router

from app.core.config import settings
from app.core.logger import logger

logger.info("Starting EDIP Backend")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(database_router)
app.include_router(
    decisions_router,
    prefix="/api/v1"
)
app.include_router(kpi_router)
app.include_router(alerts_router)
app.include_router(root_cause_router)
app.include_router(recommendations_router)
app.include_router(customer_router)
app.include_router(product_router)
app.include_router(region_router)
app.include_router(category_router)
app.include_router(discount_router)
app.include_router(growth_router)
app.include_router(dashboard_router)
app.include_router(filters_router)
app.include_router(export_router)  # Included Export Router


@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "Running"
    }