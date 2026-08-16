from sqlalchemy import Column, Integer, String
from app.core.database import Base


class DimRegion(Base):
    __tablename__ = "dim_region"

    region_id = Column(Integer, primary_key=True)
    region_name = Column(String(100))
    country = Column(String(100))