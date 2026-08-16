from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from app.core.database import Base


class FactSales(Base):

    __tablename__ = "fact_sales"

    sale_id = Column(Integer, primary_key=True)

    customer_id = Column(
        Integer,
        ForeignKey("dim_customer.customer_id")
    )

    product_id = Column(
        Integer,
        ForeignKey("dim_product.product_id")
    )

    date_id = Column(
        Integer,
        ForeignKey("dim_date.date_id")
    )

    region_id = Column(
        Integer,
        ForeignKey("dim_region.region_id")
    )

    ship_mode_id = Column(
        Integer,
        ForeignKey("dim_ship_mode.ship_mode_id")
    )

    quantity = Column(Integer)

    sales = Column(Float)

    discount = Column(Float)

    profit = Column(Float)