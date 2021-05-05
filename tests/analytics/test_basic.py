from pandas import Series

from src.analytics._return import periodic_return
from tests.raw_data.security import pbw, pbw_daily_cum_return


def test_return():
    """Unit test for user methods."""

    returns = periodic_return(Series(pbw), cumulative=True)
    assert Series.equals(returns, Series(pbw_daily_cum_return))
