from sqlalchemy.orm import Session
from tablemodels import Instrument, MarketData  # 按需 import

class InstrumentCRUD:
    @staticmethod
    def create(db: Session, data: dict):
        obj = Instrument(**data)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

# 其他表同理复制类...
