"""Test risk adjusted return analytics"""

from pandas import DataFrame, Series

from src import analytics as core
from tests.analytics.utils import get_df_results
from tests.test_data.raw_data import analytics

security_returns_df = DataFrame(analytics.returns_analytics_raw)
benchmark_series = Series(analytics.benchmark_raw)

test_returns = [security_returns_df, security_returns_df["AAPL"]]


###### Basic metrics ######


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


###### Other ratios ######


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
