from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Product(Base):

    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    price = Column(
        Integer,
        nullable=False
    )

    description = Column(
        String,
        nullable=False
    )

    image = Column(
        String,
        nullable=False
    )
    image_size = Column(
    String,
    nullable=False,
    default="medium"
    )

    category = Column(
        String,
        nullable=False
    )

    video = Column(
        String,
        default=""
    )

    featured = Column(
        Boolean,
        default=False
    )

    stock = Column(
        Integer,
        default=1
    )