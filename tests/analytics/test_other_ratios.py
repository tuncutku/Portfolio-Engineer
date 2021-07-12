"""Test other ratios"""

from pandas import DataFrame, Series

from src import analytics as core
from tests.analytics.utils import get_df_results
from tests.test_data.raw_data import analytics

security_returns_df = DataFrame(analytics.returns_analytics_raw)
benchmark_series = Series(analytics.benchmark_raw)

test_returns = [security_returns_df, security_returns_df["AAPL"]]


# def test_risk_of_ruin_ratio():
#     """Test risk of ruin ratio."""

#     df_results = get_df_results(0.07368, 0.10522)
#     for returns, results in zip(test_returns, df_results):
#         assert core.risk_of_ruin(returns).equals(results)


def test_tail_ratio():
    """Test tail ratio."""

    df_results = get_df_results(1.09382, 1.26076)
    for returns, results in zip(test_returns, df_results):
        assert core.tail_ratio(returns).equals(results)


def test_payoff_ratio():
    """Test payoff ratio."""

    df_results = get_df_results(1.11416, 1.15353)
    for returns, results in zip(test_returns, df_results):
        assert core.payoff_ratio(returns).equals(results)


def test_profit_ratio():
    """Test profit ratio."""

    df_results = get_df_results(1.00017, 0.98422)
    for returns, results in zip(test_returns, df_results):
        assert core.profit_ratio(returns).equals(results)


def test_profit_factor():
    """Test profit factor."""

    df_results = get_df_results(1.2407, 1.3514)
    for returns, results in zip(test_returns, df_results):
        assert core.profit_factor(returns).equals(results)


def test_cpc_index():
    """Test cpc index."""

    df_results = get_df_results(0.72837, 0.84109)
    for returns, results in zip(test_returns, df_results):
        assert core.cpc_index(returns).equals(results)


def test_common_sense_ratio():
    """Test common sense ratio."""

    df_results = get_df_results(1.35710, 1.70379)
    for returns, results in zip(test_returns, df_results):
        assert core.common_sense_ratio(returns).equals(results)


def test_outlier_win_ratio():
    """Test outlier win ratio."""

    df_results = get_df_results(4.61307, 3.51035)
    for returns, results in zip(test_returns, df_results):
        assert core.outlier_win_ratio(returns).equals(results)


def test_outlier_loss_ratio():
    """Test outlier loss ratio."""

    df_results = get_df_results(4.16331, 4.36509)
    for returns, results in zip(test_returns, df_results):
        assert core.outlier_loss_ratio(returns).equals(results)


def test_kelly_ratio():
    """Test kelly ratio."""

    df_results = get_df_results(0.06679, 0.10736)
    for returns, results in zip(test_returns, df_results):
        assert core.kelly_criterion(returns).equals(results)
