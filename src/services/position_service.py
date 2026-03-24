from typing import List, Optional
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..database.crud import PositionCRUD
from tablemodels.models import Position

class PositionService:
    """Position Service: Manages current positions, including retrieval, updates, and deletions."""

    @staticmethod
    def get_position(symbol: str) -> Optional[Position]:
        with SessionLocal() as db:
            return PositionCRUD.get_position(db, symbol)

    @staticmethod
    def update_or_create(
        symbol: str,
        loss: float,
        mode: str,
        volume: int,
        risk: float,
        ratio: float
    ) -> Position:
        with SessionLocal() as db:
            return PositionCRUD.create_or_update(db, symbol, loss, mode, volume, risk, ratio)

    @staticmethod
    def delete_position(symbol: str) -> int:
        with SessionLocal() as db:
            return PositionCRUD.delete_by_symbol(db, symbol)

    @staticmethod
    def get_all_positions() -> List[Position]:
        with SessionLocal() as db:
            return PositionCRUD.get_all(db)
