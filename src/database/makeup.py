# src/database/makeup.py
# Run with: python src/database/makeup.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.database.crud import InstrumentCRUD
from src.database.session import SessionLocal


db = SessionLocal()
InstrumentCRUD.create(db, exchange="SHFE", code="au")
InstrumentCRUD.create(db, exchange="SHFE", code="ag")
InstrumentCRUD.create(db, exchange="SHFE", code="cu")
InstrumentCRUD.create(db, exchange="SHFE", code="al")
InstrumentCRUD.create(db, exchange="SHFE", code="ru")
InstrumentCRUD.create(db, exchange="SHFE", code="rb")
InstrumentCRUD.create(db, exchange="SHFE", code="bu")
InstrumentCRUD.create(db, exchange="SHFE", code="ni")
InstrumentCRUD.create(db, exchange="SHFE", code="ao")


#InstrumentCRUD.create(db, exchange="DCE", code="m")
#InstrumentCRUD.create(db, exchange="DCE", code="p")
#InstrumentCRUD.create(db, exchange="DCE", code="jm")
#InstrumentCRUD.create(db, exchange="DCE", code="i")
#InstrumentCRUD.create(db, exchange="DCE", code="eg")
#InstrumentCRUD.create(db, exchange="DCE", code="eb")

#InstrumentCRUD.create(db, exchange="CZCE", code="TA")
#InstrumentCRUD.create(db, exchange="CZCE", code="MA")
#InstrumentCRUD.create(db, exchange="CZCE", code="SA")
#InstrumentCRUD.create(db, exchange="CZCE", code="FG")
#InstrumentCRUD.create(db, exchange="CZCE", code="PX")
#InstrumentCRUD.create(db, exchange="CZCE", code="SH")
#InstrumentCRUD.create(db, exchange="CZCE", code="SM")
#InstrumentCRUD.create(db, exchange="CZCE", code="CF")

InstrumentCRUD.create(db, exchange="GFEX", code="lc")
InstrumentCRUD.create(db, exchange="GFEX", code="ps")
