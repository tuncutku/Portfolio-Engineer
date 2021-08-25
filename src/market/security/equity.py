"""Equity security"""

from dataclasses import dataclass
from src.market.security.utils.base import Instrument
from src.market.types import SecurityType


@dataclass
class Equity(Instrument):
    """Form equity object."""

    def __repr__(self):
        return "Equity {}".format(self.symbol.symbol)

    @property
    def security_type(self) -> str:
        return SecurityType.equity

    # @property
    # def industry(self):
    #     pass

    # @property
    # def company(self):
    #     pass
