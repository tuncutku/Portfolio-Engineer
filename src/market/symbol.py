"""Symbol object used to extract market data."""
# pylint: disable=invalid-name

from datetime import date, timedelta
from typing import Union, TypeVar
from functools import partial
from dataclasses import dataclass

from pandas import Series, bdate_range
from pandas_datareader.data import DataReader
from yfinance import Ticker


T = TypeVar("T")
provider = partial(DataReader, data_source="yahoo")


@dataclass
class Symbol:
    """Form object to get market data of the underlying symbol."""

    symbol: str

    def __repr__(self):
        return self.symbol

    def __eq__(self: T, other: Union[str, T]):
        if isinstance(other, Symbol):
            return self.symbol == other.symbol
        if isinstance(other, str):
            return self.symbol == other
        raise ValueError(f"Cannot compare {other}.")

    @property
    def info(self) -> dict:
        """Information of the symbol."""
        return Ticker(self.symbol).info

    @property
    def is_valid(self) -> bool:
        """Valide if the ticker exist in the database source."""
        return bool(self.info.get("symbol"))

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
        raw_index = provider(name=self.symbol, start=start, end=end)
        if bday:
            date_range = bdate_range(raw_index.index.min(), raw_index.index.max())
            raw_index = raw_index.reindex(date_range).fillna(method="ffill")
        return raw_index[request].rename(self.symbol)
