from typing import List, Optional
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..database.crud import InstrumentCRUD
from tablemodels.models import Instrument

class InstrumentService:
    """Instrument Service: Manages trading instruments, including adding new instruments, retrieving instrument information, etc."""

    @staticmethod
    def add_instrument(
        exchange: str,
        code: str
    ) -> Instrument:
        with SessionLocal() as db:
            return InstrumentCRUD.create(
                db,
                exchange,
                code
            )

    @staticmethod
    def get_instrument(exchange: str, code: str) -> Optional[Instrument]:
        with SessionLocal() as db:
            return InstrumentCRUD.get_by_exchange_code(db, exchange, code)

    @staticmethod
    def get_all_instruments() -> List[Instrument]:
        with SessionLocal() as db:
            return InstrumentCRUD.get_all(db)
