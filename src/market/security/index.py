"""Exchange traded fund."""


from src.market.security.base import Security


class Index(Security):
    """Form exchange traded fund object."""

    def __repr__(self):
        return "<Index {}.>".format(self.symbol.symbol)

    @property
    def industry(self):
        """Industry of the Index."""
        return

    @property
    def holding_companies(self):
        """Major holding companies of the Index."""
        return