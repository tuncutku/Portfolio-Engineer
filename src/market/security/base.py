"""Base for securities"""
# pylint: disable=no-name-in-module

from abc import abstractmethod, ABC
from datetime import date
from pydantic import BaseModel

from src.market.basic import IndexValue, SingleValue, Currency, Symbol


class Security(BaseModel, ABC):
    """Base class for securities."""

    asset_currency: Currency
    symbol: Symbol

    @property
    def security_type(self) -> str:
        """Security type."""
        return self.__class__.__name__

    @abstractmethod
    def __repr__(self):
        """Security description."""

    @property
    def value(self) -> SingleValue:
        """Get current value of the underlying."""
        return SingleValue(self.symbol.info["regularMarketPrice"], self.asset_currency)

    def index(self, start: date, end: date = date.today()) -> IndexValue:
        """Get index of the underlying."""
        raw_index = self.symbol.index(start, end)
        return IndexValue(raw_index.rename(str(self.symbol)), self.asset_currency)
