"""Test risk adjusted return analytics"""

from pandas import DataFrame, Series

from src import analytics as core
from tests.analytics.utils import get_df_results
from tests.test_data.raw_data import analytics

security_returns_df = DataFrame(analytics.returns_analytics_raw)
benchmark_series = Series(analytics.benchmark_raw)

test_returns = [security_returns_df, security_returns_df["AAPL"]]


###### Risk-adjusted returns based on Volatility ######


def test_sharpe_ratio():
    """Test sharpe ratio."""

    df_results = get_df_results(0.07368, 0.10522)
    for returns, results in zip(test_returns, df_results):
        assert core.sharpe_ratio(returns).equals(results)


def test_modigliani_ratio():
    """Test modigliani ratio."""

    df_results = get_df_results(0.00137, 0.00196)
    for returns, results in zip(test_returns, df_results):
        assert core.modigliani_ratio(returns, benchmark_series).equals(results)


def test_treynor_ratio():
    """Test treynor ratio."""

    df_results = get_df_results(0.00170, 0.00404)
    for returns, results in zip(test_returns, df_results):
        assert core.treynor_ratio(returns, benchmark_series).equals(results)


def test_information_ratio():
    """Test information ratio."""

    df_results = get_df_results(0.06319, 0.09806)
    for returns, results in zip(test_returns, df_results):
        assert core.information_ratio(returns, benchmark_series).equals(results)


###### Risk-adjusted returns based on Value-at-Risk ######


def test_excess_var_ratio():
    """Test excess VaR ratio."""

    df_results = get_df_results(-0.04609, -0.06730)
    for returns, results in zip(test_returns, df_results):
        assert core.excess_var_ratio(returns).equals(results)


def test_conditional_sharpe_ratio():
    """Test conditional sharpe ratio."""

    df_results = get_df_results(-0.02927, -0.04268)
    for returns, results in zip(test_returns, df_results):
        assert core.conditional_sharpe_ratio(returns).equals(results)


###### Risk-adjusted returns based on partial moments ######


def test_omega_ratio():
    """Test omega ratio."""

    df_results = get_df_results(0.24057, 0.35135)
    for returns, results in zip(test_returns, df_results):
        assert core.omega_ratio(returns).equals(results)


def test_sortino_ratio():
    """Test sortino ratio."""

    df_results = get_df_results(0.10931, 0.16297)
    for returns, results in zip(test_returns, df_results):
        assert core.sortino_ratio(returns).equals(results)


def test_kappa_three_ratio():
    """Test kappa three ratio."""

    df_results = get_df_results(0.07090, 0.10706)
    for returns, results in zip(test_returns, df_results):
        assert core.kappa_three_ratio(returns).equals(results)


def test_gain_loss_ratio():
    """Test gain loss ratio."""

    df_results = get_df_results(1.2400, 1.3513)
    for returns, results in zip(test_returns, df_results):
        assert core.gain_loss_ratio(returns).equals(results)


def test_upside_potential_ratio():
    """Test upside potential ratio."""

    df_results = get_df_results(0.56342, 0.62678)
    for returns, results in zip(test_returns, df_results):
        assert core.upside_potential_ratio(returns).equals(results)


###### Risk-adjusted returns based on drawdown risk ######


def test_calmar_ratio():
    """Test calmar ratio."""

    df_results = get_df_results(-0.00612, -0.00871)
    for returns, results in zip(test_returns, df_results):
        assert core.calmar_ratio(returns).equals(results)


def test_sterling_ratio():
    """Test sterling ratio."""

    df_results = get_df_results(-0.02177, -0.03390)
    for returns, results in zip(test_returns, df_results):
        assert core.sterling_ratio(returns).equals(results)


def test_burke_ratio():
    """Test burke ratio."""

    df_results = get_df_results(0.01743, 0.02627)
    for returns, results in zip(test_returns, df_results):
        assert core.burke_ratio(returns).equals(results)


def test_recovery_factor():
    """Test recovery factor."""

    df_results = get_df_results(2.49763, 5.51576)
    for returns, results in zip(test_returns, df_results):
        assert core.recovery_factor(returns).equals(results)
