"""Test return analytics"""

from pandas import DataFrame, Series

from src.analytics import single_return, portfolio_return
from tests.test_data import raw_data
from tests.test_data.analytics import securities_df, quantities_df
from tests.test_data.raw_data import analytics

periodic_return_df = DataFrame(raw_data.periodic_return_raw)
periodic_return_cum_df = DataFrame(raw_data.periodic_return_cum_raw)

weighted_return_series = Series(raw_data.weighted_return_raw)
weighted_cum_return_series = Series(raw_data.weighted_cum_return_raw)

security_returns_df = DataFrame(analytics.returns_analytics_raw)
benchmark_series = Series(analytics.benchmark_raw)


def test_single_return():
    """Unit test for single periodic return analytics."""

    assert single_return(securities_df).equals(periodic_return_df)
    assert single_return(securities_df, cumulative=True).equals(periodic_return_cum_df)


def test_weighted_return():
    """Unit test for single weighted return analytics."""

    assert portfolio_return(securities_df, quantities_df).equals(weighted_return_series)
    assert portfolio_return(securities_df, quantities_df, cumulative=True).equals(
        weighted_cum_return_series
    )
