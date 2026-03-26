# src/database/crud.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete
from datetime import datetime, timezone

from tablemodels.models import (
    Instrument, MarketData, Plan, Orders, Position, Trade, Account, Log
)


# ==================== Instrument ====================
class InstrumentCRUD:
    @staticmethod
    def create(
        db: Session,
        exchange: str,
        code: str
    ) -> Instrument:
        obj = Instrument(
            exchange=exchange,
            code=code
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_exchange_code(db: Session, exchange: str, code: str) -> Optional[Instrument]:
        return db.execute(
            select(Instrument).where(Instrument.exchange == exchange, Instrument.code == code)
        ).scalar_one_or_none()

    @staticmethod
    def get_all(db: Session) -> List[Instrument]:
        return db.execute(select(Instrument)).scalars().all()


# ==================== MarketData ====================
class MarketDataCRUD:
    @staticmethod
    def create(db: Session, timestamp: datetime, symbol: str, category: str,
               ohlc: str, conclusion: Optional[str] = None) -> MarketData:
        obj = MarketData(
            timestamp=timestamp,
            symbol=symbol,
            category=category,
            ohlc=ohlc,
            conclusion=conclusion
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_latest_by_symbol(db: Session, symbol: str, limit: int = 1) -> List[MarketData]:
        return db.execute(
            select(MarketData)
            .where(MarketData.symbol == symbol)
            .order_by(MarketData.timestamp.desc())
            .limit(limit)
        ).scalars().all()


# ==================== Plan ====================
class PlanCRUD:
    @staticmethod
    def create(
        db: Session,
        symbol: str,
        upper: Optional[float] = None,
        lower: Optional[float] = None,
        uppertouches: Optional[int] = None,
        lowertouches: Optional[int] = None,
    ) -> Plan:
        obj = Plan(
            symbol=symbol,
            upper=upper,
            lower=lower,
            uppertouches=uppertouches,
            lowertouches=lowertouches,
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_symbol(db: Session, symbol: str) -> Optional[Plan]:
        return db.execute(select(Plan).where(Plan.symbol == symbol)).scalar_one_or_none()

    @staticmethod
    def delete_by_symbol(db: Session, symbol: str) -> int:
        result = db.execute(delete(Plan).where(Plan.symbol == symbol))
        db.commit()
        return result.rowcount

    @staticmethod
    def create_or_update(
        db: Session,
        symbol: str,
        upper: Optional[float] = None,
        lower: Optional[float] = None,
        uppertouches: Optional[int] = None,
        lowertouches: Optional[int] = None,
    ) -> Plan:
        existing = db.execute(select(Plan).where(Plan.symbol == symbol)).scalar_one_or_none()
        if existing:
            if upper is not None:
                existing.upper = upper
            if lower is not None:
                existing.lower = lower
            if uppertouches is not None:
                existing.uppertouches = uppertouches
            if lowertouches is not None:
                existing.lowertouches = lowertouches
            db.commit()
            db.refresh(existing)
            return existing
        return PlanCRUD.create(db, symbol, upper, lower, uppertouches, lowertouches)


# ==================== Order ====================
class OrdersCRUD:
    @staticmethod
    def create(db: Session, order_id: str, symbol: str, direction: str,
               price: float, volume: int, risk: float, status: str) -> Orders:
        obj = Orders(
            order_id=order_id,
            symbol=symbol,
            direction=direction,
            price=price,
            volume=volume,
            risk=risk,
            status=status
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_order_id(db: Session, order_id: str) -> Optional[Orders]:
        return db.execute(select(Orders).where(Orders.order_id == order_id)).scalar_one_or_none()

    @staticmethod
    def update_status(db: Session, order_id: str, new_status: str) -> Optional[Orders]:
        stmt = (
            update(Orders)
            .where(Orders.order_id == order_id)
            .values(status=new_status)
            .returning(Orders)
            .execution_options(synchronize_session="fetch")
        )
        result = db.execute(stmt)
        updated_order = result.scalar_one_or_none()
        db.commit()
        db.refresh(updated_order)
        return updated_order


# ==================== Position ====================
class PositionCRUD:
    @staticmethod
    def create_or_update(db: Session, symbol: str, loss: float, mode: str,
                         volume: int, risk: float, ratio: float) -> Position:
        existing = db.get(Position, symbol)
        if existing:
            existing.loss = loss
            existing.mode = mode
            existing.volume = volume
            existing.risk = risk
            existing.ratio = ratio
            db.commit()
            db.refresh(existing)
            return existing
        else:
            obj = Position(symbol=symbol, loss=loss, mode=mode, volume=volume, risk=risk, ratio=ratio)
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj

    @staticmethod
    def get_position(db: Session, symbol: str) -> Optional[Position]:
        return db.query(Position).filter(Position.symbol == symbol).first()

    @staticmethod
    def get_all(db: Session) -> List[Position]:
        return db.execute(select(Position)).scalars().all()

    @staticmethod
    def delete_by_symbol(db: Session, symbol: str) -> int:
        result = db.execute(delete(Position).where(Position.symbol == symbol))
        db.commit()
        return result.rowcount


# ==================== Trade ====================
class TradeCRUD:
    @staticmethod
    def create_open(db: Session, symbol: str, volume: int, open_price: float,
                    status: str = "open") -> Trade:
        obj = Trade(
            symbol=symbol,
            status=status,
            open_time=datetime.now(timezone.utc),
            volume=volume,
            open_price=open_price
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def close_trade(db: Session, trade_id: int, close_price: float,
                    profits: float, r_value: float, status: str = "closed") -> Optional[Trade]:
        stmt = (
            update(Trade)
            .where(Trade.id == trade_id)
            .values(
                status=status,
                close_time=datetime.now(timezone.utc),
                close_price=close_price,
                profits=profits,
                R=r_value
            )
            .returning(Trade)
            .execution_options(synchronize_session="fetch")
        )
        result = db.execute(stmt)
        closed_trade = result.scalar_one_or_none()
        db.commit()
        if closed_trade:
            db.refresh(closed_trade)
        return closed_trade

    @staticmethod
    def get_open_trades(db: Session, symbol: Optional[str] = None) -> List[Trade]:
        stmt = select(Trade).where(Trade.status == "open")
        if symbol:
            stmt = stmt.where(Trade.symbol == symbol)
        return db.execute(stmt).scalars().all()


# ==================== Account ====================
class AccountCRUD:
    @staticmethod
    def create_or_update(db: Session, account_id: str, balance: float,
                         available: float, margin: float) -> Account:
        existing = db.get(Account, account_id)
        now = datetime.now(timezone.utc)
        if existing:
            existing.balance = balance
            existing.available = available
            existing.margin = margin
            existing.update_time = now
            db.commit()
            db.refresh(existing)
            return existing
        else:
            obj = Account(
                account_id=account_id,
                balance=balance,
                available=available,
                margin=margin,
                update_time=now
            )
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj

    @staticmethod
    def get_account(db: Session, account_id: str) -> Optional[Account]:
        return db.get(Account, account_id)


# ==================== Log ====================
class LogCRUD:
    @staticmethod
    def create(db: Session, level: str, message: str, module: str) -> Log:
        obj = Log(level=level, message=message, module=module)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_recent(db: Session, limit: int = 100) -> List[Log]:
        return db.execute(
            select(Log).order_by(Log.timestamp.desc()).limit(limit)
        ).scalars().all()
