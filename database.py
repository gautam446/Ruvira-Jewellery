from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://ruvira_db_user:d3OQlGX3QrD0fs5B7MfFtjuM9ivZYkar@dpg-d8pr18jsq97s738cqdvg-a/ruvira_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()