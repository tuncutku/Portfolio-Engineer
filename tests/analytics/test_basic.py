"""Test basic analytics"""

from pandas import Series, concat

from src.analytics._return import single_periodic_return, weighted_periodic_return
from tests.raw_data.security import pbw, pbw_daily_cum_return


def test_single_return():
    """Unit test for single periodic return analytics."""

    returns = single_periodic_return(
        concat([Series(pbw, name="a"), Series(pbw, name="b")], axis=1), cumulative=True
    )
    cum_returns = single_periodic_return(
        concat([Series(pbw, name="a"), Series(pbw, name="b")], axis=1)
    )
    # assert Series.equals(returns, Series(pbw_daily_cum_return))


def test_weighted_return():
    """Unit test for single weighted return analytics."""

    returns = weighted_periodic_return(
        concat([Series(pbw, name="a"), Series(pbw, name="b")], axis=1), cumulative=True
    )