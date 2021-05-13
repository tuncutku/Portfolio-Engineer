"""Objects used to report values"""
# pylint: disable=invalid-name

from datetime import date
from typing import TypeVar
from functools import partial, cached_property
from dataclasses import dataclass

from pandas import Series, DatetimeIndex
from pandas_datareader.data import DataReader
from pandas_market_calendars import get_calendar

from src.market.types import Exchange
from src.market.symbol import Symbol


T = TypeVar("T")
provider = partial(DataReader, data_source="yahoo")


CurrencyExchangeMap = {
    "USD": Exchange.XNYS,
    "EUR": Exchange.EUREX,
    "CAD": Exchange.XTSE,
    "TRY": Exchange.XIST,
}


@dataclass
class Currency:
    """Form a currency object from a string."""

    currency: str

    def __repr__(self):
        return self.currency

    def calender(self, start: date, end: date = date.today()) -> DatetimeIndex:
        """Calender of the underlying currency."""
        exchange = CurrencyExchangeMap.get(self.currency)
        calender = get_calendar(exchange)
        return calender.valid_days(start, end)


@dataclass
class FX:
    """Form fx index object."""

    asset_currency: Currency
    numeraire_currency: Currency

    def __repr__(self):
        return f"{self.numeraire_currency}{self.asset_currency} FX Index"

    @property
    def symbol(self):
        """Generate symbol."""
        return Symbol(f"{self.numeraire_currency}{self.asset_currency}=X")

    @cached_property
    def rate(self) -> float:
        """Current fx rate."""
        request = "regularMarketPrice"
        return self.symbol.info[request]

    def index(self, start: date, end: date = date.today()) -> Series:
        """FX index."""
        return self.symbol.index(start, end)
