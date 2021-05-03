"""Equity security."""

from src.market.security.base import Security


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