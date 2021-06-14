"""Common utility functions used in views."""
# pylint: disable=invalid-name

from datetime import date
from pandas import Timestamp
from pandas.tseries.offsets import BDay

from src.market.security import Equity, Instrument, ETF, Index
from src.market.basic import Currency
from src.market import Info, Symbol

from src.market.ref_data import buy, sell


def get_business_day(date_input: date) -> date:
    """Get the closest business day by given date."""

    if date_input.weekday() in (5, 6):
        friday: Timestamp = date_input - BDay(1)
        date_input = friday.date()
    return date_input


DIRECTION_MAP = {"Buy": buy, "Sell": sell}
SECURITY_MAP = {
    "EQUITY": lambda symbol: Equity(Currency(symbol.get_info(Info.currency)), symbol),
    "ETF": lambda symbol: ETF(Currency(symbol.get_info(Info.currency)), symbol),
    "INDEX": lambda symbol: Index(Currency(symbol.get_info(Info.currency)), symbol),
}


def get_instrument(symbol: Symbol) -> Instrument:
    """Form security by given symbol."""

    f = SECURITY_MAP[symbol.get_info(Info.instrument_type)]
    return f(symbol)
