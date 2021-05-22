"""Common utility functions used in views."""
# pylint: disable=invalid-name

from datetime import date

from pandas import Timestamp
from pandas.tseries.offsets import BDay

from src.market import Symbol, Security
from src.views.utils.yfinance import security_map


def get_security(symbol: Symbol) -> Security:
    """Form security by given symbol."""

    info = symbol.info
    f = security_map[info["quoteType"]]
    return f(info)


def get_business_day(date_input: date) -> date:
    """Get the closest business day by given date."""

    if date_input.weekday() in (5, 6):
        friday: Timestamp = date_input - BDay(1)
        date_input = friday.date()
    return date_input
