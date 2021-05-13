"""Objects used to report values"""
# pylint: disable=invalid-name

from typing import Union, TypeVar
from dataclasses import dataclass
from pandas import Series, concat

from src.market.basic import Currency, FX


T = TypeVar("T")


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
            return self
        return SingleValue(self.value * FX(currency, self.currency).rate, currency)


@dataclass
class IndexValue:
    """From an index object with values."""

    index: Series
    currency: Currency

    def __repr__(self):
        start = self.index.index.min().date()
        end = self.index.index.max().date()
        return f"Index {self.currency}: {start} / {end}"

    def __eq__(self: T, other: T):
        if isinstance(other, IndexValue):
            ccy = self.currency == other.currency
            idx = Series.equals(self.index, other.index)
            return ccy and idx
        raise ValueError(f"Cannot compare {other}.")

    def __mul__(self, other: Union[float, int, Series]):
        if isinstance(other, Series):
            new_index = (self.index * other).dropna()
            return IndexValue(new_index.rename(self.index.name), self.currency)
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
            return self
        fx = FX(currency, self.currency)
        new_index = self * fx.index(self.index.index.min(), self.index.index.max())
        return IndexValue(new_index.index.rename(self.index.name), currency)

    def replace(self, data: Series) -> None:
        """Replace a value in the index."""
        for idx, value in data.items():
            if idx in self.index:
                self.index[idx] = value
