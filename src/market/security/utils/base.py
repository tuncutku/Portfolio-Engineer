"""Base for securities"""
# pylint: disable=no-name-in-module

from abc import abstractmethod, ABC
from datetime import date
from dataclasses import dataclass

from src.market.basic import Currency
from src.market.symbol import Symbol
from src.market.security.utils.value import SingleValue, IndexValue


@dataclass
class Instrument(ABC):
    """Base class for securities."""

    asset_currency: Currency
    symbol: Symbol

    # @classmethod
    # @abstractmethod
    # def generate_by_info(cls, info):
    #     """Get security by symbol info."""

    @property
    def security_type(self) -> str:
        """Instrument type."""
        return self.__class__.__name__

    @abstractmethod
    def __repr__(self):
        """Instrument description."""

    @property
    def name(self) -> str:
        """Get short name of the undelying."""
        return self.symbol.get_info("shortName")

    @property
    def value(self) -> SingleValue:
        """Get current value of the underlying."""
        return SingleValue(self.symbol.get_info("price"), self.asset_currency)

    def index(
        self,
        start: date,
        end: date = date.today(),
        request: str = "Adj Close",
        bday: bool = True,
    ) -> IndexValue:
        """Get index of the underlying."""
        return IndexValue(
            self.symbol.index(start, end, request, bday), self.asset_currency
        )
