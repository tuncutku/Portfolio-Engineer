"""Objects used to report values"""
# pylint: disable=invalid-name

from typing import Union
from dataclasses import dataclass
from pandas import DataFrame, Series, concat

from src.market.basic import Currency, FX


DataType = Union[Series, DataFrame]


@dataclass
class SingleValue:
    """Form single value object."""

    value: Union[float, int]
    currency: Currency

    def __repr__(self):
        return f"{self.value} {self.currency}"

    def __eq__(self, other) -> bool:
        if isinstance(other, SingleValue):
            ccy = self.currency == other.currency
            idx = round(self.value, 3) == round(other.value, 3)
            return ccy and idx
        raise ValueError(f"Cannot compare {other}.")

    def __mul__(self, other: Union[float, int]) -> "SingleValue":
        return SingleValue(self.value * other, self.currency)

    def __rmul__(self, other) -> "SingleValue":
        return self * other

    def __add__(self, other: Union[float, int, "SingleValue"]) -> "SingleValue":
        if isinstance(other, SingleValue):
            if self.currency != other.currency:
                raise ValueError("Cannot sum two values with different currencies.")
            return SingleValue(self.value + other.value, self.currency)
        return SingleValue(self.value + other, self.currency)

    def __radd__(self, other) -> "SingleValue":
        return self + other

    def __round__(self, n) -> "SingleValue":
        return SingleValue(round(self.value, n), self.currency)

    def to(self, currency: Currency) -> "SingleValue":
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

    def __eq__(self, other) -> bool:
        if isinstance(other, IndexValue):
            ccy = self.currency == other.currency
            _len = len(self.index) == len(other.index)
            _sum = round(sum(self.index), 3) == round(sum(other.index), 3)
            return ccy and _len and _sum
        raise ValueError(f"Cannot compare {other}.")

    def __mul__(self, other: Union[float, int]) -> "IndexValue":
        return IndexValue(self.index * other, self.currency)

    def __rmul__(self, other) -> "IndexValue":
        return self * other

    def __add__(self, other: Union[float, int, "IndexValue"]) -> "IndexValue":
        if isinstance(other, IndexValue):
            if self.currency != other.currency:
                raise ValueError("Cannot sum two values with different currencies.")
            new_index = concat([self.index, other.index])
            agg_index = new_index.groupby(new_index.index).agg("sum")
            return IndexValue(agg_index, self.currency)
        if isinstance(other, (float, int)):
            return IndexValue(self.index + other, self.currency)
        raise ValueError(f"Cannot sum: {other}")

    def __radd__(self, other) -> "IndexValue":
        return self + other

    def __round__(self, n) -> "IndexValue":
        return IndexValue(self.index.round(n), self.currency)

    def to(self, currency: Currency) -> "IndexValue":
        """Convert single value currency."""
        if self.currency == currency:
            return self
        fx = FX(currency, self.currency)
        index = self.multiply(fx.index(self.index.index.min(), self.index.index.max()))
        index.currency = currency
        return index

    def replace(self, data: Series) -> None:
        """Replace a value in the index."""
        for idx, value in data.items():
            if idx in self.index:
                self.index[idx] = value

    def multiply(self, other: Series) -> "IndexValue":
        """Multiply the underlying index with Series object."""
        new_index = (self.index * other).dropna().rename(self.index.name)
        return IndexValue(new_index, self.currency)
