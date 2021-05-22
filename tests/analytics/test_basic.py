"""Test basic analytics"""

from datetime import date
from pandas import Series, concat

from src.analytics._return import (
    periodic_return,
    weighted_periodic_return,
    holding_period_return,
)
from tests.test_data.market import portfolio_series


def test_single_return():
    """Unit test for single periodic return analytics."""

    returns = periodic_return(portfolio_series, cumulative=True)
    cum_returns = periodic_return(portfolio_series)
    # assert Series.equals(returns, Series(pbw_daily_cum_return))


def test_weighted_return():
    """Unit test for single weighted return analytics."""

    returns = weighted_periodic_return(portfolio_series, cumulative=True)


# def test_holding_period_return():
#     """Unit test for holding period return analytics."""

#     hpr_return = holding_period_return(
#         portfolio_series, date(2020, 1, 6), date(2020, 1, 22), True
#     )
