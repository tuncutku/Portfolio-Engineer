"""Objects used to report values."""
# pylint: disable=invalid-name

from datetime import date
from typing import Union, TypeVar
from functools import partial
from dataclasses import dataclass

from pandas import Series, DataFrame, DatetimeIndex
from pandas_datareader.data import DataReader
from yfinance import Ticker
from pandas_market_calendars import get_calendar

from src.market.types import Exchange


T = TypeVar("T")
provider = partial(DataReader, data_source="yahoo")


@dataclass
class Symbol:
    """Form object to get market data of the underlying symbol."""

    symbol: str

    def __repr__(self):
        return self.symbol

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, input_value):
        """Validate symbol input."""
        if isinstance(input_value, cls):
            return input_value
        if isinstance(input_value, str):
            return cls(input_value)
        raise ValueError(f"{input_value} is not supported value.")

    @property
    def info(self) -> dict:
        """Information of the symbol."""
        return Ticker(self.symbol).info

    @property
    def is_valid(self) -> bool:
        """Valide if the ticker exist in the database source."""
        return bool(self.info.get("symbol"))

    def index(self, start: date, end: date) -> DataFrame:
        """Underlying index of the symbol."""
        return provider(name=self.symbol, start=start, end=end)


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

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, input_value):
        """Validate symbol input."""
        if isinstance(input_value, cls):
            return input_value
        if isinstance(input_value, str):
            if input_value in CurrencyExchangeMap:
                return cls(input_value)
        raise ValueError(f"Given currency: {input_value} is not currenctly covered.")

    def calender(self, start: date, end: date = date.today()) -> DatetimeIndex:
        """Calender of the underlying currency."""
        exchange = CurrencyExchangeMap.get(self.currency)
        calender = get_calendar(exchange)
        return calender.valid_days(start, end)


@dataclass
class SingleValue:
    """Form single value object."""

    value: float
    currency: Currency

    def to(self: T, currency: Currency) -> T:
        """Convert single value currency."""
        symbol = Symbol(f"{self.currency}{currency}=X")
        rate = symbol.info["regularMarketPrice"]
        return SingleValue(value=self.value * rate, currency=currency)

    def __repr__(self):
        return f"{self.value} {self.currency}"

    def __mul__(self, other: Union[float, int]):
        return SingleValue(value=self.value * other, currency=self.currency)

    def __rmul__(self, other):
        return self * other

    def __add__(self: T, other: Union[float, int, T]):
        if isinstance(other, SingleValue):
            if self.currency != other.currency:
                raise ValueError("Cannot sum two values with different currencies.")
            return SingleValue(self.value + other.value, self.currency)
        return SingleValue(self.value + other, self.currency)

    def __radd__(self, other):
        return self + other


@dataclass
class IndexValue:
    """From and index object with values."""

    index: Series
    currency: Currency

    def __repr__(self):
        return f"Index {self.currency}"

    def to(self: T, currency: Currency) -> T:
        """Convert single value currency."""
        symbol = Symbol(f"{self.currency}{currency}=X")
        rate = symbol.info["regularMarketPrice"]
        return IndexValue(self.index * rate, currency)

    def __mul__(self, other: Union[float, int]):
        return IndexValue(self.index * other, self.currency)

    def __rmul__(self, other):
        return self * other

    def __add__(self: T, other: Union[float, int, T]):
        if isinstance(other, IndexValue):
            if self.currency != other.currency:
                raise ValueError("Cannot sum two values with different currencies.")
            return IndexValue(self.index + other.index, self.currency)
        if isinstance(other, (float, int)):
            return IndexValue(self.index + other, self.currency)
        raise ValueError(f"Cannot sum: {other}")

    def __radd__(self, other):
        return self + other
