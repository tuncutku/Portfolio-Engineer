"""Utility analytics functions."""

# pylint: disable=line-too-long

from math import ceil

from pandas import Series
from scipy.stats import linregress

from src.analytics import utils


@utils.analytics_result
def comp(returns: utils.PandasDataType) -> Series:
    """Calculate total compounded returns """

    returns = utils.convert_series_to_df(returns)
    return returns.apply(lambda ret: utils.non_zero_returns(ret).add(1).prod() - 1)


# TODO: display dates as well.
def _count_consecutive(returns: utils.PandasDataType) -> Series:
    """Counts consecutive dates (like cumsum() with reset on zeroes)."""

    def _count(ret: Series):
        return ret * (ret.groupby((ret != ret.shift(1)).cumsum()).cumcount() + 1)

    returns = utils.convert_series_to_df(returns)
    return returns.apply(_count)


@utils.analytics_result
def consecutive_wins(returns: utils.PandasDataType) -> Series:
    """Returns the maximum consecutive wins."""

    return _count_consecutive(returns > 0).max()


@utils.analytics_result
def consecutive_losses(returns: utils.PandasDataType) -> Series:
    """Returns the maximum consecutive losses."""

    return _count_consecutive(returns < 0).max()


@utils.analytics_result
def exposure(returns: utils.PandasDataType) -> utils.PandasDataType:
    """Returns the market exposure time (returns != 0)."""

    def _exposure(ret: Series) -> Series:
        ex = len(utils.non_zero_returns(ret)) / len(ret)
        return ceil(ex * 100) / 100

    returns = utils.convert_series_to_df(returns)
    return returns.apply(_exposure)


@utils.analytics_result
def win_rate(returns: utils.PandasDataType) -> Series:
    """Calculates the win ratio for a period."""

    def _win_rate(ret: Series) -> Series:
        ret = utils.non_zero_returns(ret)
        return len(ret[ret > 0]) / len(ret)

    returns = utils.convert_series_to_df(returns)
    return returns.apply(_win_rate)


@utils.analytics_result
def avg_return(returns: utils.PandasDataType) -> utils.PandasDataType:
    """Calculates the average return/trade return for a period."""

    returns = utils.convert_series_to_df(returns)
    return returns.apply(lambda ret: ret[ret != 0].mean())


@utils.analytics_result
def avg_win(returns: utils.PandasDataType) -> Series:
    """Calculates the average winning return/trade return for a period."""

    returns = utils.convert_series_to_df(returns)
    return returns.apply(lambda ret: ret[ret > 0].mean())


@utils.analytics_result
def avg_loss(returns: utils.PandasDataType) -> Series:
    """Calculates the average low if return/trade return for a period."""

    returns = utils.convert_series_to_df(returns)
    return abs(returns.apply(lambda ret: ret[ret < 0].mean()))


@utils.analytics_result
def cagr(returns: utils.PandasDataType) -> Series:
    """Calculates the cumulative annualized growth return (CAGR%) of access returns."""

    returns = utils.convert_series_to_df(returns)
    years = len(returns.index) / 252
    return (comp(returns) + 1.0).pow(1.0 / years) - 1


@utils.analytics_result
def skew(returns: utils.PandasDataType) -> Series:
    """Calculates skew. (the degree of asymmetry of a distribution around its mean)"""

    returns = utils.convert_series_to_df(returns)
    return returns.apply(lambda ret: utils.non_zero_returns(ret).skew())


@utils.analytics_result
def kurtosis(returns: utils.PandasDataType) -> Series:
    """Calculate kurtosis. (the degree to which a distribution peak compared to a normal distribution)"""

    returns = utils.convert_series_to_df(returns)
    return returns.apply(lambda ret: utils.non_zero_returns(ret).kurtosis())


@utils.analytics_result
def r_squared(returns: utils.PandasDataType, benchmark: Series):
    """Measures the straight line fit of the equity curve."""

    def run_regression(ret: Series):
        _, _, r_val, _, _ = linregress(ret, benchmark)
        return r_val ** 2

    returns = utils.convert_series_to_df(returns)
    return returns.apply(run_regression)
