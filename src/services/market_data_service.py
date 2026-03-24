from typing import List
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..database.crud import MarketDataCRUD
from tablemodels.models import MarketData

class MarketDataService:
    """Market Data Service: Manages market data, including saving and retrieving OHLC data, conclusions, etc."""

    @staticmethod
    def save_market_data(
        symbol: str,
        category: str,
        ohlc_text: str,
        conclusion: str,
    ) -> MarketData:
        with SessionLocal() as db:
            return MarketDataCRUD.create(
                db,
                timestamp=datetime.now(timezone.utc),
                symbol=symbol,
                category=category,
                ohlc=ohlc_text,
                conclusion=conclusion
            )

    @staticmethod
    def get_latest_data(symbol: str, limit: int = 1) -> List[MarketData]:
        with SessionLocal() as db:
            return MarketDataCRUD.get_latest_by_symbol(db, symbol, limit)
