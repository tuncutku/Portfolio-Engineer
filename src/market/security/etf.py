"""Exchange traded fund"""
# pylint: disable=duplicate-code

from src.market.security.base import Security


class ETF(Security):
    """Form exchange traded fund object."""

    def __repr__(self):
        return "<ETF {}.>".format(self.symbol.symbol)

    # @property
    # def industry(self):
    #     """Industry of the ETF."""
    #     return

    # @property
    # def holding_companies(self):
    #     """Major holding companies of the ETF."""
    #     return
