# src/services/plan_service.py
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..database.crud import PlanCRUD
from tablemodels.models import Plan

class PlanService:
    """
    Plan Service: Manages trading plans for selected instruments, including creation, retrieval, and deletion of plans. 
    Each plan corresponds to a trading opportunity identified by the market scanning process.
    """

    @staticmethod
    def create_plan(symbol: str) -> Plan:
        with SessionLocal() as db:
            existing = PlanCRUD.get_by_symbol(db, symbol)
            if existing:
                return existing
            return PlanCRUD.create(db, symbol)

    @staticmethod
    def get_plan(symbol: str) -> Optional[Plan]:
        with SessionLocal() as db:
            return PlanCRUD.get_by_symbol(db, symbol)

    @staticmethod
    def get_all_plans() -> List[Plan]:
        with SessionLocal() as db:
            return db.query(Plan).all()

    @staticmethod
    def delete_plan(symbol: str) -> int:
        with SessionLocal() as db:
            return PlanCRUD.delete_by_symbol(db, symbol)

    @staticmethod
    def exists(symbol: str) -> bool:
        with SessionLocal() as db:
            return PlanCRUD.get_by_symbol(db, symbol) is not None
