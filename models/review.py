from sqlalchemy import Column, Integer, String
from database import Base


class Review(Base):

    __tablename__ = "reviews"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_name = Column(
        String,
        nullable=False
    )

    rating = Column(
        Integer,
        nullable=False
    )

    comment = Column(
        String,
        nullable=False
    )

    product_id = Column(
        Integer,
        nullable=False
    )