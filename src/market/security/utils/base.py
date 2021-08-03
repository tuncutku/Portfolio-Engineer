"""Base for securities"""
# pylint: disable=no-name-in-module, too-many-arguments

from abc import abstractmethod, ABC
from datetime import date
from dataclasses import dataclass
from typing import Union

from pandas import Series

from src.market.types import Sector
from src.market.basic import Currency
from src.market.symbol import Symbol, Info
from src.market.security.utils.value import SingleValue, IndexValue


@dataclass
class Instrument(ABC):
    """Base class for securities."""

    asset_currency: Currency
    symbol: Symbol
    sector: Sector = Sector.other

    @abstractmethod
    def __repr__(self):
        """Instrument description."""

    @property
    def security_type(self) -> str:
        """Instrument type."""
        return self.__class__.__name__

    @property
    def name(self) -> str:
        """Get short name of the undelying."""
        return self.symbol.get_info(Info.name)

    def value(
        self, request: str = Info.price, raw: bool = False
    ) -> Union[SingleValue, float]:
        """Get current value of the underlying."""
        value = self.symbol.get_info(request)
        return value if raw else SingleValue(value, self.asset_currency)

    def index(
        self,
        start: date,
        end: date = date.today(),
        request: str = "Adj Close",
        bday: bool = True,
        raw: bool = False,
    ) -> Union[IndexValue, Series]:
        """Get index of the underlying."""
        index = self.symbol.index(start, end, request, bday)
        return index if raw else IndexValue(index, self.asset_currency)
