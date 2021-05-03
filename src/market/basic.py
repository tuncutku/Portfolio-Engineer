"""Objects used to report values."""
# pylint: disable=invalid-name

from datetime import date, timedelta
from typing import Union, TypeVar
from functools import partial, cached_property, cache
from dataclasses import dataclass

from pandas import Series, DataFrame, DatetimeIndex, concat
from pandas_datareader.data import DataReader
from yfinance import Ticker
from pandas_market_calendars import get_calendar

from src.market.types import Exchange


T = TypeVar("T")
provider = partial(DataReader, data_source="yahoo")


@dataclass
class Info:
    """Class to hold information from YFinance."""

    sector: str
    fullTimeEmployees: int
    longBusinessSummary: str
    city: str
    country: str
    website: str
    industry: str
    regularMarketPrice: str


@dataclass
class Symbol:
    """Form object to get market data of the underlying symbol."""

    symbol: str

    def __repr__(self):
        return self.symbol

    def __eq__(self, other: Union[str, T]):
        if isinstance(other, Symbol):
            return self.symbol == other.symbol
        if isinstance(other, str):
            return self.symbol == other
        raise ValueError(f"Cannot compare {other}.")

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

    def is_trading_day(self, trade_date: date) -> bool:
        """Validate if the date is a trading date."""
        start = trade_date - timedelta(3)
        end = trade_date + timedelta(3)
        index = self.index(start, end)
        return trade_date.strftime("%Y-%m-%d") in index

    def index(self, start: date, end: date) -> Series:
        """Underlying index of the symbol."""
        raw_index = provider(name=self.symbol, start=start, end=end)
        return raw_index["Adj Close"]


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
        request = "regularMarketPrice"
        return self.symbol.info[request]

    def index(self, start: date, end: date = date.today()) -> Series:
        index = self.symbol.index(start, end)
        return index.rename(self.symbol.symbol)


@dataclass
class SingleValue:
    """Form single value object."""

    value: Union[float, int]
    currency: Currency

    def __repr__(self):
        return f"{self.value} {self.currency}"

    def __eq__(self: T, other: T):
        if isinstance(other, SingleValue):
            ccy = self.currency == other.currency
            idx = self.value == other.value
            return ccy and idx
        raise ValueError(f"Cannot compare {other}.")

    def __mul__(self, other: Union[float, int]):
        return SingleValue(self.value * other, self.currency)

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

    def to(self: T, currency: Currency) -> T:
        """Convert single value currency."""
        if self.currency == currency:
            return SingleValue(self.value, self.currency)
        return SingleValue(self.value * FX(currency, self.currency).rate, currency)


@dataclass
class IndexValue:
    """From an index object with values."""

    index: Series
    currency: Currency

    def __repr__(self):
        return f"Index {self.currency} between {self.index.index.min()} - {self.index.index.max()}"

    def __eq__(self: T, other: T):
        if isinstance(other, IndexValue):
            ccy = self.currency == other.currency
            idx = Series.equals(self.index, other.index)
            return ccy and idx
        raise ValueError(f"Cannot compare {other}.")

    def __mul__(self, other: Union[float, int]):
        return IndexValue(self.index * other, self.currency)

    def __rmul__(self, other):
        return self * other

    def __add__(self: T, other: Union[float, int, T]):
        if isinstance(other, IndexValue):
            if self.currency != other.currency:
                raise ValueError("Cannot sum two values with different currencies.")
            new_index = concat([self.index, other.index])
            agg_index = new_index.groupby(new_index.index).agg("sum")
            return IndexValue(agg_index, self.currency)
        if isinstance(other, (float, int)):
            return IndexValue(self.index + other, self.currency)
        raise ValueError(f"Cannot sum: {other}")

    def __radd__(self, other):
        return self + other

    def to(self: T, currency: Currency) -> T:
        """Convert single value currency."""
        if self.currency == currency:
            return IndexValue(self.index, self.currency)
        fx = FX(currency, self.currency)
        new_index = self.multiply(
            fx.index(self.index.index.min(), self.index.index.max())
        )
        return IndexValue(new_index.index, currency)

    def replace(self, data: Series) -> None:
        """Replace a value in the index."""
        for idx, value in data.items():
            if idx in self.index:
                self.index[idx] = value

    def multiply(self: T, series: Series) -> T:
        """Multiply the index with a Series object."""
        other = series.reindex(self.index.index).fillna(method="ffill")
        return IndexValue((self.index * other).dropna(), self.currency)
