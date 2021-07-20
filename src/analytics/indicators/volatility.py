"""Volatility indicators"""


from pandas import DataFrame
from ta import volatility


def bollinger_bands(close, window=20, window_dev=2) -> DataFrame:
    """Get Bollinger bands."""

    hband = volatility.bollinger_hband(close, window, window_dev)
    lband = volatility.bollinger_lband(close, window, window_dev)
    mavg = volatility.bollinger_mavg(close, window, window_dev)
    pband = volatility.bollinger_pband(close, window, window_dev)
    wband = volatility.bollinger_wband(close, window, window_dev)
    lband_indicator = volatility.bollinger_lband_indicator(close, window, window_dev)
    hband_indicator = volatility.bollinger_hband_indicator(close, window, window_dev)
