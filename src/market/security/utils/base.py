"""Base for securities"""
# pylint: disable=no-name-in-module

from abc import abstractmethod, ABC
from datetime import date
from dataclasses import dataclass
from pandas import bdate_range

from src.market.basic import Currency
from src.market.symbol import Symbol
from src.market.security.utils.value import SingleValue, IndexValue


@dataclass
class Security(ABC):
    """Base class for securities."""

    asset_currency: Currency
    symbol: Symbol

    # @classmethod
    # @abstractmethod
    # def generate_by_info(cls, info):
    #     """Get security by symbol info."""

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

    def index(
        self,
        start: date,
        end: date = date.today(),
        request: str = "Adj Close",
        bday: bool = True,
    ) -> IndexValue:
        """Get index of the underlying."""
        index = self.symbol.index(start, end, request)
        if bday:
            date_range = bdate_range(index.index.min(), index.index.max())
            index = index.reindex(date_range).fillna(method="ffill")
        return IndexValue(index, self.asset_currency)
