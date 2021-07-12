"""Metrics"""

# pylint: disable=invalid-name


from pandas import Series

from src.analytics import basic
from src.analytics import utils


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

# TODO: investigate the ratio
# @utils.analytics_result
# def risk_of_ruin(returns: utils.PandasDataType) -> utils.PandasDataType:
#     """Calculate risk of ruin. (the likelihood of losing all one's investment capital)"""

#     def ror(ret: Series):
#         ret = utils.non_zero_returns(ret)
#         wins = basic.win_rate(ret)
#         return ((1 - wins) / (1 + wins)).pow(len(ret))

#     returns = utils.convert_series_to_df(returns)
#     return returns.apply(ror)


@utils.analytics_result
def tail_ratio(returns: utils.PandasDataType, cutoff=0.95) -> utils.PandasDataType:
    """Measures the ratio between the right (95%) and left tail (5%)."""

    def _tail_ratio(ret: Series):
        ret = utils.non_zero_returns(ret)
        return abs(ret.quantile(cutoff) / ret.quantile(1 - cutoff))

    returns = utils.convert_series_to_df(returns)
    return returns.apply(_tail_ratio)


@utils.analytics_result
def payoff_ratio(returns: utils.PandasDataType) -> utils.PandasDataType:
    """Measures the payoff ratio. (average win/average loss)"""

    return basic.avg_win(returns) / basic.avg_loss(returns)


@utils.analytics_result
def profit_ratio(returns: utils.PandasDataType) -> utils.PandasDataType:
    """Measures the profit ratio (win ratio / loss ratio) """

    def _profit_ratio(ret: Series):
        ret = utils.non_zero_returns(ret)
        wins = ret[ret > 0]
        loss = ret[ret < 0]
        win_ratio = abs(wins.mean() / wins.count())
        loss_ratio = abs(loss.mean() / loss.count())
        return win_ratio / loss_ratio

    returns = utils.convert_series_to_df(returns)
    return returns.apply(_profit_ratio)


@utils.analytics_result
def profit_factor(returns: utils.PandasDataType) -> utils.PandasDataType:
    """Measures the profit ratio (wins/loss)."""

    def _profit_factor(ret: Series):
        ret = utils.non_zero_returns(ret)
        return abs(ret[ret >= 0].sum() / ret[ret < 0].sum())

    returns = utils.convert_series_to_df(returns)
    return returns.apply(_profit_factor)


@utils.analytics_result
def cpc_index(returns: utils.PandasDataType) -> utils.PandasDataType:
    """Measures the cpc ratio. (profit factor * win % * win loss ratio)"""

    return profit_factor(returns) * basic.win_rate(returns) * payoff_ratio(returns)


@utils.analytics_result
def common_sense_ratio(returns):
    """Measures the common sense ratio (profit factor * tail ratio) """

    return profit_factor(returns) * tail_ratio(returns)


@utils.analytics_result
def outlier_win_ratio(
    returns: utils.PandasDataType, quantile=0.99
) -> utils.PandasDataType:
    """
    calculates the outlier winners ratio
    99th percentile of returns / mean positive return
    """

    def _outlier_loss_ratio(ret: Series):
        ret = utils.non_zero_returns(ret)
        return ret.quantile(quantile) / ret[ret > 0].mean()

    returns = utils.convert_series_to_df(returns)
    return returns.apply(_outlier_loss_ratio)


@utils.analytics_result
def outlier_loss_ratio(
    returns: utils.PandasDataType, quantile=0.01
) -> utils.PandasDataType:
    """
    calculates the outlier losers ratio
    1st percentile of returns / mean negative return
    """

    def _outlier_loss_ratio(ret: Series):
        ret = utils.non_zero_returns(ret)
        return ret.quantile(quantile) / ret[ret < 0].mean()

    returns = utils.convert_series_to_df(returns)
    return returns.apply(_outlier_loss_ratio)


@utils.analytics_result
def kelly_criterion(returns):
    """
    calculates the recommended maximum amount of capital that
    should be allocated to the given strategy, based on the
    Kelly Criterion (http://en.wikipedia.org/wiki/Kelly_criterion)
    """

    returns = utils.convert_series_to_df(returns)
    returns = utils.non_zero_returns(returns)
    win_loss_ratio = payoff_ratio(returns)
    win_prob = basic.win_rate(returns)
    lose_prob = 1 - win_prob
    return ((win_loss_ratio * win_prob) - lose_prob) / win_loss_ratio
