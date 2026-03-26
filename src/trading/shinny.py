# src/trading/shinny.py
# Run with: python src/trading/shinny.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
from tqsdk import TqApi, TqAccount, TqAuth, TqKq, TqSim, TqBacktest
from src.config  import Config
from src.logging import Logger

logger = Logger.get()

class Shinny:
    """
    Wrappper for TqApi,
    Provides methods to get K-line data and save it in a format suitable for LLM input,
    Provides methods to manage account and positions, and to execute trades based on LLM decisions.
    Provides three work modes: DEMO, BACKTEST, LIVE.
    """
    def __init__(self, work_mode: str = "LIVE"):
        self.work_mode = work_mode.upper()
        self.api = None


    def __enter__(self):
        config = Config.get()

        broker_password = os.getenv(config.tqsdk_account_password)
        if not broker_password:
            raise ValueError(config.tqsdk_account_password + "not found in environment variables!")
        
        tqauth_password = os.getenv(config.tqsdk_auth_password)
        if not tqauth_password:
            raise ValueError(config.tqsdk_auth_password + "not found in environment variables!")
        
        self.auth = TqAuth(config.tqsdk_auth_username, tqauth_password)
        self.backtest = None # Only used in BACKTEST mode

        if self.work_mode == "LIVE":
            self.account = TqAccount(config.tqsdk_account_broker,
                                    config.tqsdk_account_userid,
                                    broker_password)
        elif self.work_mode == "BACKTEST":
            self.account = TqSim()
            self.backtest = TqBacktest(start_time="2025-01-01", end_time="2025-12-31")
        else:
            self.account = TqKq()

        self.api = TqApi(auth=self.auth, account=self.account, backtest=self.backtest)
        logger.info(f"[Shinny] Initialized in {self.work_mode} mode with account: {config.tqsdk_account_userid}")

        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            Logger.get().error(f"[Shinny] Exception occurred: {exc_type.__name__} - {exc_val}")
        if self.api:
            self.api.close()
            self.api = None


    def get_symbol(self, exchange: str, code: str) -> str:
        """Get the latest quote (symbol of main contract) for a given exchange and code."""
        symbol = None
        symbollist = self.api.query_cont_quotes(exchange_id=exchange, product_id=code)
        
        if len(symbollist) > 0:
            symbol = symbollist[0]
        else:
            Logger.get().error(f"[Shinny] get_symbol: {exchange}.{code}, no symbol found in query_cont_quotes!")
        return symbol
    

    def get_price_precision(self, symbol: str) -> int:
        """Get the price precision (number of decimal places) for a given symbol."""
        quote = self.api.get_quote(symbol)
        return quote.price_decs
    

    def get_price_tick(self, symbol: str) -> float:
        """Get the price tick (minimum price movement) for a given symbol."""
        quote = self.api.get_quote(symbol)
        return quote.price_tick


    def get_volume_multiple(self, symbol: str) -> int:
        """Get the volume multiple (contract multiplier) for a given symbol."""
        quote = self.api.get_quote(symbol)
        return quote.volume_multiple
    

    def get_kline_data(self, symbol: str, duration_seconds: int, data_length: int) -> str:
        price_precision = self.get_price_precision(symbol)
        float_format = f"%.{price_precision}f"

        klines = self.api.get_kline_serial(symbol=symbol, duration_seconds=duration_seconds, data_length=data_length)
        df = klines[["open", 'high', 'low', "close"]].copy()
        df_transposed = df.T

        text_content = df_transposed.to_csv(sep=",", header=False, index=False, float_format=float_format)
        return text_content


if __name__ == "__main__":
    with Shinny(work_mode="DEMO") as shinny:
        #kline_text = shinny.get_kline_data(symbol="SHFE.au2606", duration_seconds=900, data_length=12)
        #print(kline_text)
        #kline_text = shinny.get_kline_data(symbol="SHFE.cu2606", duration_seconds=900, data_length=12)
        #print(kline_text)
        #kline_text = shinny.get_kline_data(symbol="SHFE.ag2606", duration_seconds=900, data_length=12)
        #print(kline_text)

        symbol1 = shinny.get_symbol(exchange="SHFE", code="ag")
        print(symbol1)
        symbol2 = shinny.get_symbol(exchange="SHFE", code="au")
        print(symbol2)

        kline_text1 = shinny.get_kline_data(symbol=symbol1, duration_seconds=900, data_length=12)
        print(kline_text1)
        kline_text2 = shinny.get_kline_data(symbol=symbol2, duration_seconds=900, data_length=12)
        print(kline_text2)