# app/database.py
from sqlmodel import create_engine, SQLModel, Session
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    # This line ensures the tables are created based on the models
    SQLModel.metadata.create_all(engine)

def get_session():
    """FastAPI dependency to get a DB session."""
    with Session(engine) as session:
        yield session