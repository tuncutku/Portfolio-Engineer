"""Exchange traded fund"""

from dataclasses import dataclass
from src.market.security.utils.base import Instrument
from src.market.types import SecurityType


@dataclass
class Index(Instrument):
    """Form exchange traded fund object."""

    def __repr__(self):
        return "Index {}".format(self.symbol.symbol)

    @property
    def security_type(self) -> str:
        return SecurityType.index

    # @property
    # def industry(self):
    #     """Industry of the Index."""
    #     return

    # @property
    # def holding_companies(self):
    #     """Major holding companies of the Index."""
    #     return
