"""Common utility functions used in views."""
# pylint: disable=invalid-name

from src.market import Currency, Equity, Instrument, ETF, Index, Info, Symbol
from src.market.ref_data import buy, sell


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
