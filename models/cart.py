from sqlalchemy import Column, Integer, String
from database import Base


class Cart(Base):

    __tablename__ = "cart"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        nullable=False
    )

    product_name = Column(
        String,
        nullable=False
    )

    product_price = Column(
        Integer,
        nullable=False
    )

    product_image = Column(
        String,
        nullable=False
    )

    quantity = Column(
        Integer,
        default=1
    )