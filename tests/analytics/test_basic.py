"""Test basic analytics"""

from datetime import date
from pandas import Series, concat, DataFrame

from src.analytics._return import (
    periodic_return,
    weighted_periodic_return,
    holding_period_return,
)

from tests.test_data import analytics
from tests.test_data.analytics import securities_df, quantities_df


def test_single_return():
    """Unit test for single periodic return analytics."""

    returns = periodic_return(securities_df)
    assert returns.equals(analytics.periodic_return_df)
    cum_returns = periodic_return(securities_df, cumulative=True)
    assert cum_returns.equals(analytics.periodic_return_cum_df)


def test_weighted_return():
    """Unit test for single weighted return analytics."""

    returns = weighted_periodic_return(securities_df, quantities_df, cumulative=True)


# def test_holding_period_return():
#     """Unit test for holding period return analytics."""

#     hpr_return = holding_period_return(
#         portfolio_df, date(2020, 1, 6), date(2020, 1, 22), True
#     )
