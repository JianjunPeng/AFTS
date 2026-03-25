# src/database/test_crud.py
# Run with: python -m src.database.test_crud

from datetime import datetime

from tablemodels  import *
from src.database import *
from src.database import SessionLocal, clear_db

def test_all_crud():
    db = SessionLocal()

    clear_db()  # 清空数据库，确保测试环境干净
    print("=== 已清空所有测试表，开始测试所有 CRUD 接口 ===\n")

    try:
        # 1. Instrument
        print("测试 Instrument...")
        instr = InstrumentCRUD.create(db, exchange="BINANCE", code="BTCUSDT", month="2605", multiplier=1)
        print(f"创建: {instr.exchange}/{instr.code}")
        found = InstrumentCRUD.get_by_exchange_code(db, "BINANCE", "BTCUSDT", "2605")
        print(f"查询: {found.code if found else 'Not found'}")
        all_instr = InstrumentCRUD.get_all(db)
        print(f"总数: {len(all_instr)}\n")

        # 2. MarketData (ohlc 现在是 Text)
        print("测试 MarketData...")
        ohlc_text = "open:65000.5,high:65500.0,low:64800.2,close:65210.75,volume:1234567"
        md = MarketDataCRUD.create(
            db,
            timestamp=datetime.utcnow(),
            symbol="BTCUSDT",
            category="1m",
            ohlc=ohlc_text,
            conclusion="突破压力位"
        )
        print(f"创建: {md.symbol} - {md.ohlc[:50]}...")
        latest = MarketDataCRUD.get_latest_by_symbol(db, "BTCUSDT", 1)
        print(f"最新一条: {latest[0].ohlc[:50] if latest else 'None'}\n")

        # 3. Plan
        print("测试 Plan...")
        plan = PlanCRUD.create(db, symbol="BTCUSDT")
        print(f"创建计划: {plan.symbol}")
        p = PlanCRUD.get_by_symbol(db, "BTCUSDT")
        print(f"查询: {p.symbol if p else 'Not found'}")
        cnt = PlanCRUD.delete_by_symbol(db, "BTCUSDT")
        print(f"删除: {cnt} 条\n")

        # 4. Order
        print("测试 Order...")
        oneorder = OrdersCRUD.create(
            db, order_id="ORD-12345", symbol="BTCUSDT", direction="buy",
            price=65200.0, volume=2, risk=500.0, status="pending"
        )
        print(f"创建订单: {oneorder.order_id}")
        o = OrdersCRUD.get_by_order_id(db, "ORD-12345")
        print(f"查询: {o.status if o else 'Not found'}")
        updated = OrdersCRUD.update_status(db, "ORD-12345", "filled")
        print(f"更新状态: {updated.status if updated else 'Fail'}\n")

        # 5. Position
        print("测试 Position...")
        pos = PositionCRUD.create_or_update(
            db, symbol="BTCUSDT", loss=64000.0, mode="trailing", volume=3,
            risk=800.0, ratio=2.5
        )
        print(f"创建/更新持仓: {pos.symbol} volume={pos.volume}")
        all_pos = PositionCRUD.get_all(db)
        print(f"当前持仓数: {len(all_pos)}")
        cnt = PositionCRUD.delete_by_symbol(db, "BTCUSDT")
        print(f"删除持仓: {cnt} 条\n")

        # 6. Trade
        print("测试 Trade...")
        trade = TradeCRUD.create_open(db, symbol="BTCUSDT", volume=1, open_price=65100.0)
        print(f"开仓: trade id={trade.id}")
        closed = TradeCRUD.close_trade(db, trade.id, close_price=66000.0, profits=900.0, r_value=1.8)
        print(f"平仓: profits={closed.profits if closed else 'Fail'}")
        opens = TradeCRUD.get_open_trades(db)
        print(f"当前开仓数: {len(opens)}\n")

        # 7. Account
        print("测试 Account...")
        acc = AccountCRUD.create_or_update(
            db, account_id="ACC-001", balance=100000.0, available=95000.0, margin=5000.0
        )
        print(f"账户: balance={acc.balance}")
        acc2 = AccountCRUD.get_account(db, "ACC-001")
        print(f"查询: available={acc2.available if acc2 else 'None'}\n")

        # 8. Log
        print("测试 Log...")
        log = LogCRUD.create(db, level="INFO", message="系统启动完成", module="main")
        print(f"日志: {log.message}")
        recent = LogCRUD.get_recent(db, 5)
        print(f"最近日志数: {len(recent)}\n")

        print("=== 所有测试完成，无明显异常 ===")

    except Exception as e:
        print(f"测试过程中出错: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    test_all_crud()
