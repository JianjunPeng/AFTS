from typing import List, Optional
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..database.crud import TradeCRUD
from tablemodels.models import Trade
from datetime import datetime, timezone

class TradeService:
    """Trade Service: Manages trade history, including opening and closing trades, retrieving open trades, etc."""

    @staticmethod
    def open_trade(symbol: str, volume: int, open_price: float) -> Trade:
        with SessionLocal() as db:
            return TradeCRUD.create_open(db, symbol, volume, open_price)

    @staticmethod
    def close_trade(
        trade_id: int,
        close_price: float,
        profits: float,
        r_value: float,
        status: str = "closed"
    ) -> Optional[Trade]:
        with SessionLocal() as db:
            return TradeCRUD.close_trade(db, trade_id, close_price, profits, r_value, status)

    @staticmethod
    def get_open_trades(symbol: Optional[str] = None) -> List[Trade]:
        with SessionLocal() as db:
            return TradeCRUD.get_open_trades(db, symbol)
