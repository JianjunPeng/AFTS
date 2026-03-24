from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config.config import Config

config = Config()
engine = create_engine(config.db_url, echo=False, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def clear_db():
    """Clear all data from the database (for testing purposes)"""
    from tablemodels import Base
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def init_db():
    """Initialize database tables (for development use)"""
    from tablemodels import Base
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()