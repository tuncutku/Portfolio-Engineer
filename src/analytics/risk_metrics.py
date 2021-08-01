"""Risk metrics"""

from numpy import cov
from scipy.stats import norm
from pandas import Series, DataFrame
from src.analytics import utils


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


def drawdown(returns: DataFrame) -> Series:
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
