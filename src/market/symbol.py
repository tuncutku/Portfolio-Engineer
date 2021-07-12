"""Symbol object used to extract market data."""
# pylint: disable=invalid-name, pointless-statement, too-many-instance-attributes

from datetime import date, timedelta
from typing import Union
from dataclasses import dataclass
from functools import cached_property

import requests

from pandas import DataFrame, Series, bdate_range
from pandas_datareader._utils import RemoteDataError
from pandas_datareader.yahoo.daily import YahooDailyReader
from pandas_datareader.yahoo.quotes import YahooQuotesReader

USER_AGENT = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
        " Chrome/91.0.4472.124 Safari/537.36"
    )
}
sesh = requests.Session()
sesh.headers.update(USER_AGENT)


@dataclass
class Info:
    """Requests to pull information from yfinance."""

    currency = "currency"
    price = "price"
    name = "shortName"
    instrument_type = "quoteType"
    market_open = "regularMarketOpen"
    time_zone = "exchangeTimezoneShortName"
    volume = "regularMarketVolume"

    # Option requests
    underlying_symbol = "underlyingSymbol"
    expire_date = "expireDate"
    strike = "strike"


@dataclass
class Symbol:
    """Form object to get market data of the underlying symbol."""

    symbol: str

    def __repr__(self):
        return self.symbol

    def __eq__(self, other: Union[str, "Symbol"]) -> bool:
        if isinstance(other, Symbol):
            return self.symbol == other.symbol
        if isinstance(other, str):
            return self.symbol == other
        raise ValueError(f"Cannot compare {other}.")

    @cached_property
    def info(self) -> DataFrame:
        """Information of the symbol."""
        provider = YahooQuotesReader(self.symbol, session=sesh)
        return provider.read()

    def get_info(self, request: str) -> Union[str, float]:
        """Get a specific request from info."""
        raw_info = self.info[request]
        return raw_info.item()

    @property
    def is_valid(self) -> bool:
        """Valide if the ticker exists."""
        try:
            self.info
            return True
        except (IndexError, RemoteDataError):
            return False

    def is_trading_day(self, trade_date: date) -> bool:
        """Validate if the date is a trading date."""
        start = trade_date - timedelta(3)
        end = trade_date + timedelta(3)
        index = self.index(start, end, bday=False)
        return trade_date.strftime("%Y-%m-%d") in index

    def index(
        self, start: date, end: date, request: str = "Adj Close", bday: bool = True
    ) -> Series:
        """Underlying index of the symbol."""
        provider = YahooDailyReader(self.symbol, start=start, end=end, session=sesh)
        raw_data = provider.read()
        raw_index = raw_data[request]
        raw_index.rename(self.symbol, inplace=True)
        if bday:
            raw_index = raw_index.reindex(
                bdate_range(start, end), method="ffill"
            ).bfill()
        return raw_index
