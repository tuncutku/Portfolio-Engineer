"""Base for securities."""
# pylint: disable=no-name-in-module
from abc import abstractmethod, ABC
from datetime import date
from pydantic import BaseModel

from src.market.basic import IndexValue, SingleValue, Currency, Symbol


class Observable(BaseModel, ABC):
    """Base class for securities."""

    asset_currency: Currency

    @abstractmethod
    def __repr__(self):
        """Short description of underlying."""

    @property
    @abstractmethod
    def value(self) -> SingleValue:
        """Get current value of the underlying."""

    @abstractmethod
    def index(self, start: date, end: date = date.today()) -> IndexValue:
        """Get index of the underlying."""


class Security(Observable):
    """Base class for securities."""

    symbol: Symbol

    @property
    def value(self):
        return SingleValue(self.symbol.info["regularMarketPrice"], self.asset_currency)

    def index(self, start: date, end: date = date.today()):
        index = self.symbol.index(start, end)["Close"]
        return IndexValue(index.rename(str(self.symbol)), self.asset_currency)
