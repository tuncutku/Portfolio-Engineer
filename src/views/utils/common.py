"""Common utility functions used in views."""
# pylint: disable=invalid-name

from src.market import Symbol, Instrument
from src.views.utils.yfinance import security_map


def get_security(symbol: Symbol) -> Instrument:
    """Form security by given symbol."""

    get_instrument = security_map[symbol.get_info("quoteType")]
    return get_instrument(symbol)
