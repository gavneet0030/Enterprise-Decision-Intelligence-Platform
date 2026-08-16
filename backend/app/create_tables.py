from app.core.database import Base, engine

# Import all models
from app.models.customer import DimCustomer
from app.models.product import DimProduct
from app.models.date import DimDate
from app.models.region import DimRegion
from app.models.sales import FactSales

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("Done ✅")