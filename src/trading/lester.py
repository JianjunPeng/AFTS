# src/trading/lester.py
# Run with: python src/trading/lester.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from datetime  import datetime, timezone
from src.model import LLM
from src.services import *
from src.logging  import Logger
from src.config   import Config
from src.trading.shinny import Shinny

class Lester:
    """
    This is the core business class for AFTS trading system, 
    responsible for managing the overall trading logic and workflow. 
    It integrates with various services to perform market scanning, 
    decision making, trade execution, and account management. 
    It also uses LLM for decision support and Logger for logging business events.
    """

    def __init__(self):
        self.log_service = LogService
        self.position_service = PositionService
        self.trade_service = TradeService
        self.order_service = OrderService
        self.instrument_service = InstrumentService
        self.market_data_service = MarketDataService
        self.account_service = AccountService
        self.plan_service = PlanService


    def __enter__(self):
        self.config = Config.get()
        self.logger = Logger().get()
        self.llm = LLM()
        self.log_business("INFO", "Lester initialized.", module="trading.lester")
        return self
    

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            Logger.get().error(f"Lester exception: {exc_type.__name__} - {exc_val}")


    def log_business(self, level: str = "INFO", message: str = "", module: str = "trading.lester"):
        """Record business events to the database"""
        self.log_service.log(level=level, message=message, module=module)
        self.logger.log(level, f"[Lester] Business log: {message} (module: {module})")


    def log_data(self, symbol: str, category: str, data: str, conclusion: str = ""):
        """Record market data to the database"""
        self.market_data_service.save_market_data(symbol=symbol, category=category, ohlc_text=data, conclusion=conclusion)
        self.logger.info(f"[Lester] Market data: {symbol} - {category} - {conclusion}")

    # ==================== 后续会实现的业务方法 ====================
    # 这些方法是交易系统的核心业务逻辑，目前先定义接口，后续会逐步实现具体逻辑。
    def scan_market(self):
        """
        Scan the market, save data, and log the event.
        1. Get market data for the given symbol in database table "instrument".
        2. Save the market data to the database table "market_data" for future analysis.
        3. Call LLM to analyze the market data and get insights for decision making.
        4. If the results from LLM indicate a trading opportunity, put the symbol into "plan" table for later processing.

        This method will be called periodically (e.g., every day before market open) 
        to keep the market data updated and to provide fresh insights for trading decisions.
        """
        module_str = "trading.lester.scan"
        instruments = self.instrument_service.get_all_instruments()

        newplans = []
        
        with Shinny(work_mode=self.config.work_mode) as shinny:
            for inst in instruments:
                symbol = shinny.get_symbol(exchange=inst.exchange, code=inst.code)
                if not symbol:
                    self.log_business(level="WARNING", message=f"Skipping instrument with invalid symbol: {inst}", module=module_str)
                    continue

                kline_data = shinny.get_kline_data(symbol, self.config.advisor_duration_scan, self.config.advisor_datalenth_scan)
                scan_result = self.llm.Scan(kline_data)

                # Save the market data and scan results to the database for future analysis and traceability
                result_str = str(scan_result)
                self.log_data(symbol=symbol, category="scan", data=kline_data, conclusion=result_str)
                self.log_business(message=f"Market data saved: {symbol} - {result_str}", module=module_str)

                # If LLM indicates a trading opportunity, create a trading plan and log the event
                if scan_result and scan_result.get("hasRange") == True:
                    self.plan_service.create_plan(symbol=symbol)
                    self.log_business(level="CRITICAL", message=f"Trading plan created: {symbol}", module=module_str)
                    newplans.append(symbol)

            self.log_business(message=f"Scan completed: {newplans} added to TradingPlan", module=module_str)


    def decide(self, symbol: str):
        """决策是否交易"""
        pass

    def execute_loss(self, symbol: str):
        """止损/止盈处理"""
        pass

    def update_account(self):
        """更新账户信息"""
        pass

if __name__ == "__main__":
    with Lester() as lester:
        lester.scan_market()