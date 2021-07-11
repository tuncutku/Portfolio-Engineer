"""Test basic analytics"""

from pandas import DataFrame, Series

from src import analytics as core
from tests.analytics.utils import get_df_results
from tests.test_data.raw_data import analytics

returns_df = DataFrame(analytics.returns_analytics_raw)
security_returns_df = DataFrame(analytics.returns_analytics_raw)
benchmark_series = Series(analytics.benchmark_raw)
test_returns = [security_returns_df, security_returns_df["AAPL"]]


def test_compounded_return():
    """Test compounded return."""

    df_results = get_df_results(0.78493, 3.34404)
    for returns, results in zip(test_returns, df_results):
        assert core.comp(returns).equals(results)


def test_consecutive():
    """Test consecutive wins and losses."""

    result = core.consecutive_wins(returns_df)
    assert result.equals(Series({"AAPL": 7, "TSLA": 6}))
    result = core.consecutive_losses(returns_df)
    assert result.equals(Series({"AAPL": 4, "TSLA": 6}))


def test_exposure():
    """Test exposure."""

    result = core.exposure(returns_df)
    assert result.equals(Series({"AAPL": 0.97, "TSLA": 0.97}))


def test_win_average_rate():
    """Test rates."""

    items = [
        ({"AAPL": 0.52691, "TSLA": 0.53955}, core.win_rate),
        ({"AAPL": 0.00200, "TSLA": 0.00546}, core.avg_return),
        ({"AAPL": 0.01952, "TSLA": 0.03892}, core.avg_win),
        ({"AAPL": 0.01752, "TSLA": 0.03374}, core.avg_loss),
    ]

    for benchmark, func in items:
        result = func(returns_df)
        assert result.equals(Series(benchmark))


def test_cagr():
    """Test compounded annual growth rate."""

    df_results = get_df_results(0.49021, 1.74920)
    for returns, results in zip(test_returns, df_results):
        assert core.cagr(returns).equals(results)


def test_skew():
    """Test skew."""

    df_results = get_df_results(0.01351, -0.04669)
    for returns, results in zip(test_returns, df_results):
        assert core.skew(returns).equals(results)


def test_kurtosis():
    """Test kurtosis."""

    df_results = get_df_results(4.30845, 2.64057)
    for returns, results in zip(test_returns, df_results):
        assert core.kurtosis(returns).equals(results)


def test_r_squared():
    """Test r-squared."""

    df_results = get_df_results(0.65380, 0.23567)
    for returns, results in zip(test_returns, df_results):
        assert core.r_squared(returns, benchmark_series).equals(results)
