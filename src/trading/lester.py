# src/trading/lester.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from datetime  import datetime, timezone
from src.model import LLM
from src.services import *
from src.logging  import Logger

class Lester:
    """AFTS 交易核心业务类"""

    def __init__(self):
        self.logger = Logger()
        self.llm = LLM()
        
        # 业务服务层
        self.log_service = LogService
        self.position_service = PositionService
        self.trade_service = TradeService
        self.order_service = OrderService
        self.instrument_service = InstrumentService
        self.market_data_service = MarketDataService
        self.account_service = AccountService

        self.logger.info("Lester 交易核心初始化完成")
        self.log_service.log("INFO", "Lester 交易系统启动", module="trading.lester")

    def log_business(self, level: str, message: str, module: str = "lester"):
        """记录业务事件到数据库"""
        self.log_service.log(level=level, message=message, module=module)

    # ==================== 后续会实现的业务方法 ====================
    def scan_market(self, symbol: str):
        """扫描行情 + 保存数据 + 记录日志"""
        pass

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
    lester = Lester()
    lester.log_business("INFO", "这是一个测试日志", module="test")
    lester.scan_market("AAPL")