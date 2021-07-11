"""Test return analytics"""


from pandas import DataFrame, Series

from src import analytics as core
from tests.analytics.utils import get_df_results
from tests.test_data.raw_data import analytics

security_returns_df = DataFrame(analytics.returns_analytics_raw)
benchmark_series = Series(analytics.benchmark_raw)

test_returns = [security_returns_df, security_returns_df["AAPL"]]


def test_volatility():
    """Test volatility."""

    df_results = get_df_results(0.02612, 0.05019)
    for returns, results in zip(test_returns, df_results):
        assert core.volatility(returns).equals(results)


def test_alpha():
    """Test alpha."""

    df_results = get_df_results(0.00086, 0.00405)
    for returns, results in zip(test_returns, df_results):
        assert core.alpha(returns, benchmark_series).equals(results)


def test_beta():
    """Test beta."""

    df_results = get_df_results(1.13451, 1.30837)
    for returns, results in zip(test_returns, df_results):
        assert core.beta(returns, benchmark_series).equals(results)


def test_lpm():
    """Test beta."""

    df_results = get_df_results(0.01387, 0.02041)
    for returns, results in zip(test_returns, df_results):
        assert core.lpm(returns, 0.01).equals(results)


def test_hpm():
    """Test beta."""

    df_results = get_df_results(0.00579, 0.01570)
    for returns, results in zip(test_returns, df_results):
        assert core.hpm(returns, 0.01).equals(results)


def test_var():
    """Test value at risk."""

    df_results = get_df_results(-0.04176, -0.07847)
    for returns, results in zip(test_returns, df_results):
        assert core.var(returns).equals(results)


def test_cvar():
    """Test conditional value at risk."""

    df_results = get_df_results(-0.06576, -0.12373)
    for returns, results in zip(test_returns, df_results):
        assert core.cvar(returns).equals(results)


def test_max_drawdown():
    """Test maximum drawdown."""

    df_results = get_df_results(-0.31427, -0.60627)
    for values, results in zip(test_returns, df_results):
        assert core.max_drawdown(values).equals(results)


def test_average_drawdown():
    """Test average drawdown."""

    df_results = get_df_results(-0.08840, -0.15579)
    for values, results in zip(test_returns, df_results):
        assert core.avg_drawdown(values).equals(results)


def test_average_square_drawdown():
    """Test average sqaure drawdown."""

    df_results = get_df_results(0.01219, 0.04042)
    for values, results in zip(test_returns, df_results):
        assert core.avg_squared_drawdown(values).equals(results)
