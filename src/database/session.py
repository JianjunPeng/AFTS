from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config.config import Config
from tablemodels import Base

engine = create_engine(Config.get().db_url, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clear_db():
    """Clear all data from the database (for testing purposes)"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def init_db():
    """Initialize database tables (for development use)"""
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()