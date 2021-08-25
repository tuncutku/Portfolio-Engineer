"""Risk adjusted metrics"""

# pylint: disable=invalid-name


from pandas import Series
from numpy import cov
from scipy.stats import norm

from src.analytics import basic, utils


###### Basic metrıcs ######


@utils.analytics_result
def volatility(returns: utils.PandasDataType) -> Series:
    """Volatility of daily returns."""

    return utils.convert_series_to_df(returns).std()


@utils.analytics_result
def alpha(returns: utils.PandasDataType, benchmark: Series) -> Series:
    """Calculate alpha."""

    returns = utils.convert_series_to_df(returns)
    return returns.mean() - beta(returns, benchmark) * benchmark.mean()


@utils.analytics_result
def beta(returns: utils.PandasDataType, benchmark: Series) -> Series:
    """Beta of daily returns."""

    def get_beta(ret: Series):
        concat_df = utils.combine_return_and_benchmark(ret, benchmark)
        matrix = cov(concat_df.iloc[:, 0], concat_df.iloc[:, 1])
        return matrix[0, 1] / matrix[1, 1]

    returns = utils.convert_series_to_df(returns)
    return returns.apply(get_beta)


@utils.analytics_result
def lpm(returns: Series, threshold: float, order: int = 1) -> Series:
    """Lower partial moment of the returns. Link:
    https://breakingdownfinance.com/finance-topics/performance-measurement/lower-partial-moment/
    """

    returns = utils.convert_series_to_df(returns)
    diff = threshold - returns
    diff = diff.clip(lower=0)
    return (diff ** order).sum() / len(returns)


@utils.analytics_result
def hpm(returns: Series, threshold: float, order: int = 1) -> Series:
    """Higher partial moment of the returns."""

    returns = utils.convert_series_to_df(returns)
    diff = returns - threshold
    diff = diff.clip(lower=0)
    return (diff ** order).sum() / len(returns)


@utils.analytics_result
def var(returns: utils.PandasDataType, sigma=1, confidence=0.95) -> Series:
    """
    calculates the daily value-at-risk
    (variance-covariance calculation with confidence n)
    """
    # Historical VaR
    # def var(returns, alpha):
    #     sorted_returns = sort(returns)
    #     index = int(alpha * len(sorted_returns))
    #     return abs(sorted_returns[index])

    def get_var(ret: Series):
        ret = utils.non_zero_returns(ret)
        return norm.ppf(1 - confidence, ret.mean(), sigma * ret.std())

    returns = utils.convert_series_to_df(returns)
    return returns.apply(get_var)


@utils.analytics_result
def cvar(returns: utils.PandasDataType, sigma=1, confidence=0.95) -> Series:
    """Conditional daily value-at-risk (aka expected shortfall) which
    quantifies the amount of tail risk an investment"""

    # This method calculates the condition VaR of the returns
    # def cvar(returns, alpha):
    #     sorted_returns = numpy.sort(returns)
    #     index = int(alpha * len(sorted_returns))
    #     sum_var = sorted_returns[0]
    #     for i in range(1, index):
    #         sum_var += sorted_returns[i]
    #     return abs(sum_var / index)

    returns = utils.convert_series_to_df(returns)
    value_at_risk = var(returns, sigma, confidence)

    def get_cvar(ret: Series):
        ret = utils.non_zero_returns(ret)
        return ret[ret < value_at_risk[ret.name]].mean()

    return returns.apply(get_cvar)


def drawdown(returns: utils.PandasDataType) -> Series:
    """Calculate drawdown."""

    values = (returns + 1).cumprod()
    return (values / values.expanding(min_periods=0).max()) - 1


@utils.analytics_result
def max_drawdown(returns: utils.PandasDataType) -> Series:
    """Calculate the maximum drawdown."""

    returns = utils.convert_series_to_df(returns)
    return drawdown(returns).min()


@utils.analytics_result
def avg_drawdown(returns: utils.PandasDataType) -> Series:
    """Calculate the average drawdown."""

    returns = utils.convert_series_to_df(returns)
    return drawdown(returns).mean()


@utils.analytics_result
def avg_squared_drawdown(returns: utils.PandasDataType) -> Series:
    """Calculate the average squared drawdown."""

    returns = utils.convert_series_to_df(returns)
    return drawdown(returns).pow(2).mean().round(5)


###### Risk-adjusted returns based on Volatility ######


@utils.analytics_result
def sharpe_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate daily sharpe ratio from daily returns."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / volatility(returns)


@utils.analytics_result
def modigliani_ratio(
    returns: utils.PandasDataType, benchmark: Series, rf: float = 0.0
) -> Series:
    """Calculate modigliani ratio."""

    returns = utils.convert_series_to_df(returns)
    return sharpe_ratio(returns, rf) * float(volatility(benchmark)) + rf


@utils.analytics_result
def treynor_ratio(
    returns: utils.PandasDataType, benchmark: Series, rf: float = 0.0
) -> Series:
    """Calculate daily treynor ratio from daily returns."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / beta(returns, benchmark)


@utils.analytics_result
def information_ratio(returns: utils.PandasDataType, benchmark: Series) -> Series:
    """Calculate daily information ratio."""

    returns = utils.convert_series_to_df(returns)
    diff_rets = returns.sub(benchmark, axis=0)
    return diff_rets.mean() / volatility(diff_rets)  # Denomiator is tracking error.


###### Risk-adjusted returns based on Value-at-Risk ######


@utils.analytics_result
def excess_var_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate Excess return VaR."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / var(returns)


@utils.analytics_result
def conditional_sharpe_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate conditional sharpe ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / cvar(returns)


###### Risk-adjusted returns based on partial moments ######


@utils.analytics_result
def omega_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate Omega ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / lpm(returns, rf, 1)


@utils.analytics_result
def sortino_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate Sortino ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / lpm(returns, rf, 2).pow(0.5)


@utils.analytics_result
def kappa_three_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate Kappa three ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / lpm(returns, rf, 3).pow(1 / 3)


@utils.analytics_result
def gain_loss_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate gain loss ratio."""

    returns = utils.convert_series_to_df(returns)
    return hpm(returns, rf, 1) / lpm(returns, rf, 1)


@utils.analytics_result
def upside_potential_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate upside potential ratio."""

    returns = utils.convert_series_to_df(returns)
    return hpm(returns, rf, 1) / lpm(returns, rf, 2).pow(0.5)


###### Risk-adjusted returns based on drawdown risk ######


@utils.analytics_result
def calmar_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate calmar ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / max_drawdown(returns)


@utils.analytics_result
def sterling_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate average drawdown ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / avg_drawdown(returns)


@utils.analytics_result
def burke_ratio(returns: utils.PandasDataType, rf: float = 0.0) -> Series:
    """Calculate burke ratio."""

    returns = utils.convert_series_to_df(returns)
    return (returns - rf).mean() / avg_squared_drawdown(returns).pow(0.5)


@utils.analytics_result
def recovery_factor(returns: utils.PandasDataType) -> utils.PandasDataType:
    """Calculate recovery factor which shows how fast the strategy recovers from drawdowns."""

    returns = utils.convert_series_to_df(returns)
    return basic.comp(returns) / abs(max_drawdown(returns))


###### Other ratios ######


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
