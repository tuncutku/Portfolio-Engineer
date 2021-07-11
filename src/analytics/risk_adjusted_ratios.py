"""Risk adjusted metrics"""

# pylint: disable=invalid-name


from pandas import Series
from src.analytics import utils
from src.analytics import risk_metrics as rm
from src.analytics.basic import comp


###### Risk-adjusted returns based on Volatility ######


@utils.analytics_result
def sharpe_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate daily sharpe ratio from daily returns."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.volatility(returns)


@utils.analytics_result
def modigliani_ratio(
    returns: utils.PandasDataType, benchmark: Series, rf: float = 0.0
) -> Series:
    """Calculate modigliani ratio."""

    returns = utils.convert_series_to_df(returns)
    return sharpe_ratio(returns, rf) * float(rm.volatility(benchmark)) + rf


@utils.analytics_result
def treynor_ratio(
    returns: utils.PandasDataType, benchmark: Series, rf: float = 0.0
) -> Series:
    """Calculate daily treynor ratio from daily returns."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.beta(returns, benchmark)


@utils.analytics_result
def information_ratio(returns: utils.PandasDataType, benchmark: Series) -> Series:
    """Calculate daily information ratio."""

    returns = utils.convert_series_to_df(returns)
    diff_rets = returns.sub(benchmark, axis=0)
    return diff_rets.mean() / rm.volatility(diff_rets)  # Denomiator is tracking error.


###### Risk-adjusted returns based on Value-at-Risk ######


@utils.analytics_result
def excess_var_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate Excess return VaR."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.var(returns)


@utils.analytics_result
def conditional_sharpe_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate conditional sharpe ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.cvar(returns)


###### Risk-adjusted returns based on partial moments ######


@utils.analytics_result
def omega_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate Omega ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.lpm(returns, rf, 1)


@utils.analytics_result
def sortino_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate Sortino ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.lpm(returns, rf, 2).pow(0.5)


@utils.analytics_result
def kappa_three_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate Kappa three ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.lpm(returns, rf, 3).pow(1 / 3)


@utils.analytics_result
def gain_loss_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate gain loss ratio."""

    returns = utils.convert_series_to_df(returns)
    return rm.hpm(returns, rf, 1) / rm.lpm(returns, rf, 1)


@utils.analytics_result
def upside_potential_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate upside potential ratio."""

    returns = utils.convert_series_to_df(returns)
    return rm.hpm(returns, rf, 1) / rm.lpm(returns, rf, 2).pow(0.5)


###### Risk-adjusted returns based on drawdown risk ######


@utils.analytics_result
def calmar_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate calmar ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.max_drawdown(returns)


@utils.analytics_result
def sterling_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate average drawdown ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.avg_drawdown(returns)


@utils.analytics_result
def burke_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate burke ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / rm.avg_squared_drawdown(returns).pow(0.5)


@utils.analytics_result
def recovery_factor(returns: utils.PandasDataType) -> utils.PandasDataType:
    """Calculate recovery factor which shows how fast the strategy recovers from drawdowns."""

    returns = utils.convert_series_to_df(returns)
    return comp(returns) / abs(rm.max_drawdown(returns))
