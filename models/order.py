from sqlalchemy import Column, Integer, String
from database import Base


class Order(Base):

    __tablename__ = "orders"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_name = Column(
        String,
        nullable=False
    )

    phone = Column(
        String,
        nullable=False
    )

    address = Column(
        String,
        nullable=False
    )

    product_name = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        default=1
    )

    total_price = Column(
        Integer,
        nullable=False
    )

    payment_method = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        default="Pending"
    )