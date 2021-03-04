# from src.market_data.base import BaseProvider
import yfinance
from typing import List
from functools import partial
from datetime import datetime, timedelta
from pandas_datareader import data
import pandas as pd

provider = partial(data.DataReader, data_source="yahoo")


class YFinance:
    def __init__(self, symbols: List[str], source: str = "yahoo"):

        self.tickers = symbols
        self.info_providers = [yfinance.Ticker(ticker) for ticker in self.tickers]
        self.quote_provider = partial(
            data.DataReader, name=self.tickers, data_source="yahoo"
        )

    @property
    def is_valid(self) -> bool:
        """Valide if the tickers exist in the database source."""
        validate = list()
        for provider in self.info_providers:
            try:
                provider.info
                validate.append(True)
            except:
                validate.append(False)
        return all(validate)

    def info(self) -> dict:
        """Get ticker informations."""
        info = dict()
        for provider in self.info_providers:
            info[provider.ticker] = provider.info
        return info

    def get_current_quotes(self, decimal: int = 5) -> pd.DataFrame:
        """Get current market prices."""
        df = pd.DataFrame()
        for provider in self.info_providers:
            raw_df = provider.history(period="5d", interval="5m")
            df[provider.ticker] = raw_df["Close"]
        return df.tail(1).round(decimal)

    def get_historical_quotes(
        self,
        start: datetime,
        end: datetime = None,
        decimal: int = 5,
    ):
        raw_df = self.quote_provider(start=start, end=end)
        return raw_df["Adj Close"].round(decimal)
