from sqlalchemy import Column, Integer, String
from database import Base


class Coupon(Base):

    __tablename__ = "coupons"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    code = Column(
        String,
        unique=True,
        nullable=False
    )

    discount = Column(
        Integer,
        nullable=False
    )