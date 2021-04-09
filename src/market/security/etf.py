"""Exchange traded fund."""

from datetime import date
from pandas import Series
from pydantic.dataclasses import dataclass

from src.market.utils.base import Security
from src.market.symbol import Symbol


@dataclass
class ETF(Security):
    """Form exchange traded fund object."""

    symbol: Symbol

    # @property
    # def industry(self):
    #     pass

    # @property
    # def holding_companies(self):
    #     pass

    def __repr__(self):
        return "<ETF {}.>".format(self.symbol.symbol)

    @property
    def short_name(self) -> str:
        """Short description of the underlying etf."""
        return self.symbol.info["shortName"]

    @property
    def currency(self) -> str:
        return self.symbol.info["currency"]

    @property
    def current_value(self) -> float:
        return self.symbol.info["regularMarketPrice"]

    def index(self, start: date, end: date = date.today()) -> Series:
        index = self.symbol.index(start, end)["Close"]
        return index.rename(self.symbol.symbol)
