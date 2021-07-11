"""Utilities for analytics"""

# pylint: disable=invalid-name, bare-except

from functools import wraps
from enum import Enum
from typing import Union

from numpy import NaN
from pandas import Series, DataFrame, concat

PandasDataType = Union[Series, DataFrame]
BenchmarkType = Union[Series, float]


def combine_return_and_benchmark(returns: Series, benchmark: Series) -> DataFrame:
    """Combine return series and benchmark series."""

    concat_df = concat([returns, benchmark], axis=1)
    return concat_df.loc[(concat_df != 0).any(axis=1)]


def convert_series_to_df(series: PandasDataType) -> DataFrame:
    """Convert Series object to Dataframe."""

    return series.to_frame() if isinstance(series, Series) else series


def non_zero_returns(series: Series) -> Series:
    """Get non zero returns."""

    return series[series != 0]


def validate_analytics_input(raw_input: PandasDataType) -> DataFrame:
    """Validate analytics result."""

    if not isinstance(raw_input, (DataFrame, Series)):
        raise ValueError
    raw_input = convert_series_to_df(raw_input)
    if len(raw_input.index) == 0:
        raise ValueError
    return raw_input


def validate_analytics_result(result: Series, raw_input: DataFrame) -> Series:
    """Validate analytics result."""

    if len(raw_input.columns) != len(result.index):
        raise ValueError
    return result


def analytics_result(func):
    """Decorator for rounding result and error handling."""

    @wraps(func)
    def decorator(*args, **kwargs):
        try:
            raw_input = validate_analytics_input(args[0])
            raw_result = func(*args, **kwargs)
            result = validate_analytics_result(raw_result, raw_input)
            return result.round(5)
        except:
            return NaN

    return decorator


class Period(Enum):
    """Periods used for resampling."""

    daily = "B"
    weekly = "W-FRI"
    monthly = "BM"
    yearly = "BY"
