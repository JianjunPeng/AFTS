# src/services/test_services.py
# Run with: python -m src.services.test_services
# Run with: pytest --cov=crud --cov-report=term-missing -v
# Run with: pytest src/services/test_services.py::test_all_services
# Run with: pytest src/services/test_services.py

from src.database import clear_db
from tablemodels  import Base
from src.services import *


def test_all_services():
    clear_db()  # 清空数据库，确保测试环境干净
    print("=== 已清空并重建数据库，开始测试 Services ===\n")

    try:
        # 1. InstrumentService
        print("测试 InstrumentService...")
        instr = InstrumentService.add_instrument(
            "BINANCE",
            "BTCUSDT",
            "2509",
            1,
            fluctuation=0.5,
            marginrate=0.12,
        )
        print(f"添加品种: {instr.exchange}/{instr.code}/{instr.month}")
        found = InstrumentService.get_instrument("BINANCE", "BTCUSDT", "2509")
        print(f"查询品种: {found.code if found else 'Not found'}")
        print(f"品种总数: {len(InstrumentService.get_all_instruments())}\n")
        assert found is not None
        assert found.exchange == "BINANCE"
        assert found.code == "BTCUSDT"
        assert found.month == "2509"
        assert found.multiplier == 1
        assert found.fluctuation == 0.5
        assert found.marginrate == 0.12

        # 2. MarketDataService
        print("测试 MarketDataService...")
        ohlc_text = "open:65000.5,high:65500.0,low:64800.2,close:65210.75,volume:1234567"
        md = MarketDataService.save_market_data(
            symbol="BTCUSDT",
            category="1m",
            ohlc_text=ohlc_text,
            conclusion="突破新高"
        )
        print(f"保存行情: {md.symbol} - {md.ohlc[:60]}...")
        latest = MarketDataService.get_latest_data("BTCUSDT", 1)
        print(f"最新行情: {latest[0].ohlc[:60] if latest else 'None'}\n")
        assert latest is not None
        assert latest[0].symbol == "BTCUSDT"
        assert latest[0].category == "1m"
        assert latest[0].ohlc == ohlc_text
        assert latest[0].conclusion == "突破新高"

        # 3. PositionService
        print("测试 PositionService...")
        pos = PositionService.update_or_create(
            symbol="BTCUSDT",
            loss=64000.0,
            mode="fixed",
            volume=2,
            risk=600.0,
            ratio=2.8
        )
        print(f"更新持仓: {pos.symbol} volume={pos.volume}")
        all_pos = PositionService.get_all_positions()
        print(f"当前持仓数量: {len(all_pos)}")
        assert all_pos is not None
        assert len(all_pos) == 1
        assert all_pos[0].symbol == "BTCUSDT"
        assert all_pos[0].loss == 64000.0
        assert all_pos[0].mode == "fixed"
        assert all_pos[0].volume == 2
        assert all_pos[0].risk == 600.0
        assert all_pos[0].ratio == 2.8
        PositionService.delete_position("BTCUSDT")
        print("已删除持仓\n")
        assert PositionService.get_all_positions() == []

        # 4. OrderService
        print("测试 OrderService...")
        order = OrderService.create_order(
            order_id="ORD-20250323-001",
            symbol="BTCUSDT",
            direction="buy",
            price=65200.0,
            volume=2,
            risk=550.0,
            status="pending"
        )
        print(f"创建委托: {order.order_id}")
        o = OrderService.get_order("ORD-20250323-001")
        print(f"查询委托状态: {o.status if o else 'Not found'}")
        assert o is not None
        assert o.order_id == "ORD-20250323-001"
        assert o.symbol == "BTCUSDT"
        assert o.direction == "buy"
        assert o.price == 65200.0
        assert o.volume == 2
        assert o.risk == 550.0
        assert o.status == "pending"
        updated = OrderService.update_order_status("ORD-20250323-001", "filled")
        print(f"更新后状态: {updated.status if updated else 'Fail'}\n")
        assert updated is not None
        assert updated.status == "filled"

        # 5. TradeService
        print("测试 TradeService...")
        trade = TradeService.open_trade(symbol="BTCUSDT", volume=2, open_price=65200.0)
        print(f"开仓成功，trade id={trade.id}")
        open_trades = TradeService.get_open_trades("BTCUSDT")
        print(f"当前开仓数量: {len(open_trades)}")
        assert open_trades is not None
        assert len(open_trades) == 1
        assert open_trades[0].id == trade.id
        assert open_trades[0].symbol == "BTCUSDT"
        assert open_trades[0].volume == 2
        assert open_trades[0].open_price == 65200.0
        closed = TradeService.close_trade(
            trade_id=trade.id,
            close_price=65800.0,
            profits=1200.0,
            r_value=2.18
        )
        print(f"平仓成功，盈亏={closed.profits if closed else 'Fail'}\n")
        open_trades_after = TradeService.get_open_trades("BTCUSDT")
        print(f"平仓后开仓数量: {len(open_trades_after)}")
        assert open_trades_after is not None
        assert len(open_trades_after) == 0

        # 6. AccountService
        print("测试 AccountService...")
        acc = AccountService.update_or_create_account(
            account_id="ACC-001",
            balance=150000.0,
            available=142000.0,
            margin=8000.0
        )
        print(f"账户更新: balance={acc.balance}, available={acc.available}")
        acc2 = AccountService.get_account("ACC-001")
        print(f"查询账户可用资金: {acc2.available if acc2 else 'None'}\n")
        assert acc2 is not None
        assert acc2.account_id == "ACC-001"
        assert acc2.balance == 150000.0
        assert acc2.available == 142000.0
        assert acc2.margin == 8000.0

        # 7. LogService
        print("测试 LogService...")
        LogService.log("INFO", "系统启动完成，准备进入交易", "main")
        LogService.log("WARNING", "BTCUSDT 价格接近止损线", "risk.control")
        LogService.log("INFO", "Decide 开仓 BTCUSDT 2手", "lester.decide")
        print("业务日志已写入数据库\n")

        # 8. PlanService
        print("测试 PlanService...")
        plan = PlanService.create_plan(symbol="BTCUSDT", upper=70000.0, lower=62000.0, uppertouches=1, lowertouches=0)
        print(f"创建交易计划: {plan.symbol}")
        
        p = PlanService.get_plan("BTCUSDT")
        print(f"查询计划: {p.symbol if p else 'Not found'}")
        assert p is not None
        assert p.symbol == "BTCUSDT"
        assert p.upper == 70000.0
        assert p.lower == 62000.0
        assert p.uppertouches == 1
        assert p.lowertouches == 0
        
        all_plans = PlanService.get_all_plans()
        print(f"当前计划品种数量: {len(all_plans)}")
        assert all_plans is not None
        assert len(all_plans) == 1
        assert all_plans[0].symbol == "BTCUSDT"
        assert all_plans[0].upper == 70000.0
        assert all_plans[0].lower == 62000.0
        assert all_plans[0].uppertouches == 1
        assert all_plans[0].lowertouches == 0

        exists = PlanService.exists("BTCUSDT")
        print(f"BTCUSDT 是否在计划中: {exists}")
        assert exists == True
        
        # 测试重复创建（不应报错）
        PlanService.create_plan("BTCUSDT", upper=3000.0, lower=2000.0, uppertouches=2, lowertouches=3)
        print("重复创建计划测试通过\n")
        p = PlanService.get_plan("BTCUSDT")
        assert p is not None
        assert p.symbol == "BTCUSDT"
        assert p.upper == 3000.0  # 已更新
        assert p.lower == 2000.0  # 已更新
        assert p.uppertouches == 2  # 已更新
        assert p.lowertouches == 3  # 已更新
        

        print("=== 所有 Services 测试通过！===")

    except Exception as e:
        print(f"测试失败: {e}")
        raise
    finally:
        # 可选：不关闭 session，让测试结束后仍能查看数据
        pass


if __name__ == "__main__":
    test_all_services()
