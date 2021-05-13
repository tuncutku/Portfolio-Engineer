"""Base for securities"""
# pylint: disable=no-name-in-module

from abc import abstractmethod, ABC
from datetime import date
from dataclasses import dataclass

from src.market.basic import Currency
from src.market.symbol import Symbol
from src.market.security.utils.context import SingleValue, IndexValue


@dataclass
class Security(ABC):
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
        return IndexValue(self.symbol.index(start, end), self.asset_currency)
