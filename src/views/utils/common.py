"""Common utility functions used in views."""
# pylint: disable=invalid-name

from src.market import Symbol, Info, Instrument
from src.views.utils.yfinance import security_map


def get_security(symbol: Symbol) -> Instrument:
    """Form security by given symbol."""

    get_instrument = security_map[symbol.get_info(Info.instrument_type)]
    return get_instrument(symbol)
