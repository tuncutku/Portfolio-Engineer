"""Test analytics utilities"""

from math import isnan
from pandas import DataFrame, Series

from src import analytics as core
from tests.test_data.raw_data import analytics

security_returns_df = DataFrame(analytics.returns_analytics_raw)
benchmark_series = Series(analytics.benchmark_raw)


def test_decorator():
    """Test decorator."""

    wrong_input = security_returns_df[1:]
    assert isnan(core.sharpe_ratio(wrong_input, benchmark_series))
