from sqlalchemy import Column, Integer, String

from app.core.database import Base


class DimShipMode(Base):
    __tablename__ = "dim_ship_mode"

    ship_mode_id = Column(Integer, primary_key=True)

    ship_mode = Column(String(100), nullable=False)