"""Test return analytics"""


from src.analytics import periodic_return, weighted_periodic_return

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

    returns = weighted_periodic_return(securities_df, quantities_df)
    assert returns.equals(analytics.weighted_return_series)
    cum_returns = weighted_periodic_return(
        securities_df, quantities_df, cumulative=True
    )
    assert cum_returns.equals(analytics.weighted_cum_return_series)


# def test_holding_period_return():
#     """Unit test for holding period return analytics."""

#     hpr_return = holding_period_return(
#         portfolio_df, date(2020, 1, 6), date(2020, 1, 22), True
#     )
