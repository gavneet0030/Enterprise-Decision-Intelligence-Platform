from sqlalchemy import Column, Integer, String
from app.core.database import Base


class DimCustomer(Base):
    __tablename__ = "dim_customer"

    customer_id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    email = Column(String(120))
    city = Column(String(100))
    country = Column(String(100))
    segment = Column(String(50))