"""Utilities for indicators"""

from functools import wraps

from numpy import array, amin, amax
from pandas import DataFrame, Series, concat


def true_range(high: Series, low: Series, prev_close: Series) -> Series:
    """True range."""

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    return DataFrame(data={"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)


def sma(series: Series, periods: int) -> Series:
    """Simple moving average."""

    return series.rolling(window=periods, min_periods=periods).mean()


def ema(series: Series, periods: int) -> Series:
    """Exponential moving average."""

    return series.ewm(span=periods, min_periods=periods, adjust=False).mean()


def get_min(series1: Series, series2: Series) -> Series:
    """Find min value between two lists for each index"""

    series1 = array(series1)
    series2 = array(series2)

    return Series(amin([array(series1), array(series2)], axis=0))


def get_max(series1: Series, series2: Series) -> Series:
    """Find max value between two lists for each index"""

    series1 = array(series1)
    series2 = array(series2)

    return Series(amax([array(series1), array(series2)], axis=0))
