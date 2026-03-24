import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database.crud import InstrumentCRUD
from src.database.session import SessionLocal


db = SessionLocal()
InstrumentCRUD.create(db, exchange="SHFE", code="au", month="2605", multiplier=1000)
InstrumentCRUD.create(db, exchange="SHFE", code="ag", month="2605", multiplier=15)
InstrumentCRUD.create(db, exchange="SHFE", code="cu", month="2605", multiplier=5)
InstrumentCRUD.create(db, exchange="SHFE", code="al", month="2605", multiplier=5)
InstrumentCRUD.create(db, exchange="SHFE", code="ru", month="2605", multiplier=10)
InstrumentCRUD.create(db, exchange="SHFE", code="rb", month="2605", multiplier=10)
InstrumentCRUD.create(db, exchange="SHFE", code="bu", month="2605", multiplier=10)
InstrumentCRUD.create(db, exchange="SHFE", code="ni", month="2605", multiplier=1)
InstrumentCRUD.create(db, exchange="SHFE", code="ao", month="2605", multiplier=20)

InstrumentCRUD.create(db, exchange="DCE", code="m", month="2605", multiplier=10)
InstrumentCRUD.create(db, exchange="DCE", code="p", month="2605", multiplier=10)
InstrumentCRUD.create(db, exchange="DCE", code="jm", month="2605", multiplier=60)
InstrumentCRUD.create(db, exchange="DCE", code="i", month="2605", multiplier=100)
InstrumentCRUD.create(db, exchange="DCE", code="eg", month="2605", multiplier=10)
InstrumentCRUD.create(db, exchange="DCE", code="eb", month="2605", multiplier=5)

InstrumentCRUD.create(db, exchange="CZCE", code="TA", month="2605", multiplier=5)
InstrumentCRUD.create(db, exchange="CZCE", code="MA", month="2605", multiplier=10)
InstrumentCRUD.create(db, exchange="CZCE", code="SA", month="2605", multiplier=20)
InstrumentCRUD.create(db, exchange="CZCE", code="FG", month="2605", multiplier=20)
InstrumentCRUD.create(db, exchange="CZCE", code="PX", month="2605", multiplier=5)
InstrumentCRUD.create(db, exchange="CZCE", code="SH", month="2605", multiplier=30)
InstrumentCRUD.create(db, exchange="CZCE", code="SM", month="2605", multiplier=5)
InstrumentCRUD.create(db, exchange="CZCE", code="CF", month="2605", multiplier=5)

InstrumentCRUD.create(db, exchange="GFEX", code="lc", month="2605", multiplier=1)
InstrumentCRUD.create(db, exchange="GFEX", code="ps", month="2605", multiplier=3)
