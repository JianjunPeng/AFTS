# src/services/log_service.py
from typing import Optional
from sqlalchemy.orm import Session
from ..database.session import SessionLocal
from ..database.crud import LogCRUD

class LogService:
    """Business Event Log Service: Records key trading-related events to the database"""

    @staticmethod
    def log(
        level: str,
        message: str,
        module: str = "business",
        extra: Optional[dict] = None
    ):
        """
        Records business events to the Log table
        level: INFO / WARNING / ERROR / CRITICAL
        message: Event description
        module: Business module name, e.g., lester.decide, risk.control
        """
        level = level.upper()
        if level not in ["INFO", "WARNING", "ERROR", "CRITICAL"]:
            level = "INFO"

        with SessionLocal() as db:
            LogCRUD.create(
                db=db,
                level=level,
                message=message,
                module=module
            )
