# from src.market_data.base import BaseProvider
import yfinance
from datetime import datetime, timedelta


class YFinance:
    def __init__(self, symbol):
        self.symbol = symbol
        self.provider = yfinance.Ticker(symbol)

    @property
    def is_valid(self):
        try:
            self.provider.info
        except:
            return False
        return True

    def info(self) -> dict:
        return self.provider.info

    def get_quote(self, decimal: int = 5) -> float:
        raw_quote = self.provider.history(period="5d", interval="5m")
        return round(float(raw_quote["Close"].head(1)), decimal)

    def get_historical_quote(
        self,
        start: datetime,
        end: datetime = None,
        date_format: str = "%Y-%m-%d",
        decimal: int = 5,
    ):
        if end is None:
            end = start + timedelta(days=1)
        raw_quote = self.provider.history(
            start=start.strftime(date_format),
            end=end.strftime(date_format),
        )

        return round(float(raw_quote["Close"].head(1)), decimal)