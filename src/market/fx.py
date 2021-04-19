"""FX Index."""

from datetime import date
from pandas import Series, DatetimeIndex
from src.market.base import Observable
from src.market.basic import IndexValue, SingleValue, Currency, Symbol


class FX(Observable):
    """Form fx index object."""

    numeraire_currency: Currency

    def __str__(self):
        return f"{self.numeraire_currency}{self.asset_currency}"

    def __repr__(self):
        return f"{self.numeraire_currency}{self.asset_currency} FX Index"

    @property
    def symbol(self):
        """Generate symbol."""
        return Symbol(f"{self.numeraire_currency}{self.asset_currency}=X")

    @property
    def value(self):
        request = "regularMarketPrice"
        return SingleValue(self.symbol.info[request], self.numeraire_currency)

    def index(self, start: date, end: date = date.today()):
        index = self.symbol.index(start, end)["Close"]
        return IndexValue(index.rename(self.symbol.symbol), self.asset_currency)
