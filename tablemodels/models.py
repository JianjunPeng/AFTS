from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Instrument(Base):
    __tablename__ = "instrument"
    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange = Column(String(10), nullable=False)
    code = Column(String(10), nullable=False)
    month = Column(String(6))
    multiplier = Column(Integer)

class MarketData(Base):
    __tablename__ = "market_data"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    symbol = Column(String(20), nullable=False)
    category = Column(String(20))
    ohlc = Column(Text)
    conclusion = Column(Text)

class Plan(Base):
    __tablename__ = "plan"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), unique=True, nullable=False)

class Orders(Base):
    __tablename__ = "orders"
    order_id = Column(String(50), primary_key=True)
    symbol = Column(String(20), nullable=False)
    direction = Column(String(10))   # buy/sell
    price = Column(Float)
    volume = Column(Integer)
    risk = Column(Float)
    status = Column(String(20))
    insert_time = Column(DateTime, default=datetime.utcnow)

class Position(Base):
    __tablename__ = "position"
    symbol = Column(String(20), primary_key=True)
    loss = Column(Float)
    mode = Column(String(20))
    volume = Column(Integer)
    risk = Column(Float)
    ratio = Column(Float)

class Trade(Base):
    __tablename__ = "trade"
    id = Column(Integer, primary_key=True, autoincrement=True)
    symbol = Column(String(20), nullable=False)
    status = Column(String(20))
    open_time = Column(DateTime)
    volume = Column(Integer)
    open_price = Column(Float)
    close_time = Column(DateTime, nullable=True)
    close_price = Column(Float, nullable=True)
    profits = Column(Float)
    R = Column(Float)

class Account(Base):
    __tablename__ = "account"
    account_id = Column(String(50), primary_key=True)
    balance = Column(Float)
    available = Column(Float)
    margin = Column(Float)
    update_time = Column(DateTime, default=datetime.utcnow)

class Log(Base):
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String(10))
    message = Column(Text)
    module = Column(String(50))
    
