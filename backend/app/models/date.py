from sqlalchemy import Column, Integer, Date
from app.core.database import Base


class DimDate(Base):
    __tablename__ = "dim_date"

    date_id = Column(Integer, primary_key=True)
    full_date = Column(Date)