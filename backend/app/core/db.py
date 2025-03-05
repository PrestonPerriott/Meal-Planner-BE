from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy_utils import database_exists, create_database
from backend.app.core.config import settings
import backend.app.data.model.grocery
from typing import Generator

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URL))

def init_db() -> None:
    """Initializes the database with the settings from the config module
    """
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        print(f"Database does not exist, creating database: {engine.url}")
        create_database(engine.url)
    
    print(f"Database exists: {engine.url}")
    SQLModel.metadata.create_all(engine)
    
def get_db() -> Generator[Session, None, None]:
    try:
        with Session(engine) as session:
            yield session
    finally:
        session.close()
        
def get_db_session() -> Session:
    """Returns a new database session"""
    return Session(engine)