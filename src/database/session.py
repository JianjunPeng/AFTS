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

# 初始化表（开发时用）
def init_db():
    from tablemodels import Base
    Base.metadata.create_all(bind=engine)
