"""Metrics"""

# pylint: disable=invalid-name


from numpy import sqrt, divide, maximum, isnan, Inf, cov
from numpy.linalg import norm
from pandas import DataFrame, concat, Series

from src.analytics import basic
from src.analytics.utils import PandasDataType, BenchmarkType


# def ulcer_index(returns: PandasDataType) -> PandasDataType:
#     """ calculates the ulcer index score (downside risk measurment) """
#     dd = 1.0 - returns / returns.cummax()
#     return sqrt(divide((dd ** 2).sum(), returns.shape[0] - 1))


# def ulcer_performance_index(returns: PandasDataType) -> PandasDataType:
#     """
#     calculates the ulcer index score
#     (downside risk measurment)
#     """
#     dd = 1.0 - returns / returns.cummax()
#     ulcer = sqrt(divide((dd ** 2).sum(), returns.shape[0] - 1))
#     return returns.mean() / ulcer


def risk_of_ruin(returns: PandasDataType) -> PandasDataType:
    """Calculate risk of ruin. (the likelihood of losing all one's investment capital)"""

    wins = basic.win_rate(returns)
    return ((1 - wins) / (1 + wins)) ** len(returns)


def tail_ratio(returns: PandasDataType, cutoff=0.95) -> PandasDataType:
    """
    measures the ratio between the right
    (95%) and left tail (5%).
    """

    return abs(returns.quantile(cutoff) / returns.quantile(1 - cutoff))


def payoff_ratio(returns: PandasDataType) -> PandasDataType:
    """ measures the payoff ratio (average win/average loss) """

    return basic.avg_win(returns) / basic.avg_loss(returns)


def profit_ratio(returns: PandasDataType) -> PandasDataType:
    """ measures the profit ratio (win ratio / loss ratio) """

    wins = returns[returns >= 0]
    loss = returns[returns < 0]

    win_ratio = abs(wins.mean() / wins.count())
    loss_ratio = abs(loss.mean() / loss.count())

    return win_ratio / loss_ratio


def profit_factor(returns: PandasDataType) -> PandasDataType:
    """ measures the profit ratio (wins/loss) """

    return abs(returns[returns >= 0].sum() / returns[returns < 0].sum())


def cpc_index(returns: PandasDataType) -> PandasDataType:
    """
    measures the cpc ratio
    (profit factor * win % * win loss ratio)
    """
    return profit_factor(returns) * basic.win_rate(returns) * payoff_ratio(returns)


def common_sense_ratio(returns):
    """ measures the common sense ratio (profit factor * tail ratio) """
    return profit_factor(returns) * tail_ratio(returns)


def outlier_win_ratio(returns: PandasDataType, quantile=0.99) -> PandasDataType:
    """
    calculates the outlier winners ratio
    99th percentile of returns / mean positive return
    """
    return returns.quantile(quantile).mean() / returns[returns >= 0].mean()


def outlier_loss_ratio(returns: PandasDataType, quantile=0.01) -> PandasDataType:
    """
    calculates the outlier losers ratio
    1st percentile of returns / mean negative return
    """
    return returns.quantile(quantile).mean() / returns[returns < 0].mean()


def kelly_criterion(returns):
    """
    calculates the recommended maximum amount of capital that
    should be allocated to the given strategy, based on the
    Kelly Criterion (http://en.wikipedia.org/wiki/Kelly_criterion)
    """
    win_loss_ratio = payoff_ratio(returns)
    win_prob = basic.win_rate(returns)
    lose_prob = 1 - win_prob

    return ((win_loss_ratio * win_prob) - lose_prob) / win_loss_ratio
