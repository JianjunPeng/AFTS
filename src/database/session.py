import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.config import Config
from tablemodels import Base
import argparse

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
    parser = argparse.ArgumentParser(description="数据库管理工具")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    parser_init = subparsers.add_parser("init", help="初始化数据库")
    parser_clear = subparsers.add_parser("clear", help="清空数据库")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_db()
    elif args.command == "clear":
        clear_db()