"""Exchange traded fund"""

from dataclasses import dataclass
from src.market.security.utils.base import Instrument
from src.market.types import SecurityType


@dataclass
class ETF(Instrument):
    """Form exchange traded fund object."""

    def __repr__(self):
        return "ETF {}".format(self.symbol.symbol)

    @property
    def security_type(self) -> str:
        return SecurityType.etf

    # @property
    # def industry(self):
    #     """Industry of the ETF."""
    #     return

    # @property
    # def holding_companies(self):
    #     """Major holding companies of the ETF."""
    #     return
