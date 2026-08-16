from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class DimProduct(Base):
    __tablename__ = "dim_product"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100))
    category = Column(String(100))
    unit_price = Column(Float)