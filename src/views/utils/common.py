"""Common utility functions used in views."""
# pylint: disable=invalid-name

from src.market import Symbol, Instrument
from src.views.utils.yfinance import security_map


def get_security(symbol: Symbol) -> Instrument:
    """Form security by given symbol."""

    info = symbol.info
    f = security_map[info["quoteType"]]
    return f(info)
