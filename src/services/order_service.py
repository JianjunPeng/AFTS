from typing import Optional
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..database.crud import OrdersCRUD
from tablemodels.models import Orders

class OrderService:
    """Order Service: Manages order creation, retrieval, and status updates"""

    @staticmethod
    def create_order(
        order_id: str,
        symbol: str,
        direction: str,
        price: float,
        volume: int,
        risk: float,
        status: str = "pending"
    ) -> Orders:
        with SessionLocal() as db:
            return OrdersCRUD.create(db, order_id, symbol, direction, price, volume, risk, status)

    @staticmethod
    def get_order(order_id: str) -> Optional[Orders]:
        with SessionLocal() as db:
            return OrdersCRUD.get_by_order_id(db, order_id)

    @staticmethod
    def update_order_status(order_id: str, new_status: str) -> Optional[Orders]:
        with SessionLocal() as db:
            return OrdersCRUD.update_status(db, order_id, new_status)
