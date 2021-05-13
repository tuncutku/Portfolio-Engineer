"""Equity security"""

from dataclasses import dataclass
from src.market.security.utils.base import Security


@dataclass
class Equity(Security):
    """Form equity object."""

    def __repr__(self):
        return "<Equity {}.>".format(self.symbol.symbol)

    # @property
    # def industry(self):
    #     pass

    # @property
    # def company(self):
    #     pass
