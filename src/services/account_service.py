from typing import Optional
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..database.crud import AccountCRUD
from tablemodels.models import Account
from datetime import datetime, timezone

class AccountService:
    """Account Information Service: Manages account information, including balance, available funds, margin, etc."""

    @staticmethod
    def update_or_create_account(
        account_id: str,
        balance: float,
        available: float,
        margin: float
    ) -> Account:
        with SessionLocal() as db:
            return AccountCRUD.create_or_update(db, account_id, balance, available, margin)

    @staticmethod
    def get_account(account_id: str) -> Optional[Account]:
        with SessionLocal() as db:
            return AccountCRUD.get_account(db, account_id)
