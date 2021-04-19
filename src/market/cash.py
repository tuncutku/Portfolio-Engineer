"""Cash."""

from datetime import date
from pandas import Series, date_range

from src.market.base import Observable
from src.market.basic import IndexValue, SingleValue


class Cash(Observable):
    """Form cash object."""

    def __repr__(self):
        return "<Cash in {}.>".format(self.asset_currency)

    @property
    def value(self):
        return SingleValue(1, self.asset_currency)

    def index(self, start: date, end: date = date.today()):
        _range = date_range(start, end)
        calender = self.asset_currency.calender
        return IndexValue(Series(), self.asset_currency)
