"""Metrics"""

# pylint: disable=invalid-name

from pandas.core.series import Series
from scipy.stats import linregress
from numpy import sqrt, divide, maximum, isnan, Inf, cov
from numpy.linalg import norm
from pandas import DataFrame, concat

from src.analytics.utils import PandasDataType
from src.analytics.basic import exposure, remove_outliers, win_rate, volatility

# ======= Basic Metrics =======


def sharpe(
    returns: PandasDataType, rf: float = 0.0, annualize=True, trading_year_days=252
) -> PandasDataType:
    """Calculates the sharpe ratio of access returns. Rf is assumed to
    be expressed in yearly (annualized) terms"""

    res = (returns - rf).mean() / returns.std()
    return res * sqrt(trading_year_days) if annualize else res


def sortino(
    returns: PandasDataType, rf: float = 0, annualize=True, trading_year_days=252
) -> PandasDataType:
    """
    calculates the sortino ratio of access returns

    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms

    Calculation is based on this paper by Red Rock Capital
    http://www.redrockcapital.com/Sortino__A__Sharper__Ratio_Red_Rock_Capital.pdf
    """

    returns = returns - rf
    downside = (returns[returns < 0] ** 2).sum() / len(returns)
    res = returns.mean() / sqrt(downside)

    return res * sqrt(trading_year_days) if annualize else res


def adjusted_sortino(
    returns: PandasDataType, rf: float = 0, annualize=True, trading_year_days=252
) -> PandasDataType:
    """
    Jack Schwager's version of the Sortino ratio allows for
    direct comparisons to the Sharpe. See here for more info:
    https://archive.is/wip/2rwFW
    """
    data = sortino(
        returns,
        rf=rf,
        annualize=annualize,
        trading_year_days=trading_year_days,
    )
    return data / sqrt(2)


def gain_to_pain_ratio(
    returns: PandasDataType, rf: float = 0, resolution="D"
) -> PandasDataType:
    """
    Jack Schwager's GPR. See here for more info:
    https://archive.is/wip/2rwFW
    """
    returns = (returns - rf).resample(resolution).sum()
    downside = abs(returns[returns < 0].sum())
    return returns.sum() / downside


def cagr(returns: PandasDataType, compounded=True) -> PandasDataType:
    """
    calculates the communicative annualized growth return
    (CAGR%) of access returns
    """

    if compounded:
        total = comp(total)
    else:
        total = _np.sum(total)

    years = (returns.index[-1] - returns.index[0]).days / 365.0

    res = abs(total + 1.0) ** (1.0 / years) - 1

    if isinstance(returns, DataFrame):
        res = _pd.Series(res)
        res.index = returns.columns

    return res


def risk_adj_return(returns: PandasDataType) -> PandasDataType:
    """
    calculates the risk-adjusted return of access returns
    (CAGR / exposure. takes time into account.)
    """
    return cagr(returns) / exposure(returns)


def skew(returns: PandasDataType) -> PandasDataType:
    """
    calculates returns' skewness
    (the degree of asymmetry of a distribution around its mean)
    """
    return returns.skew()


def kurtosis(returns: PandasDataType) -> PandasDataType:
    """
    calculates returns' kurtosis
    (the degree to which a distribution peak compared to a normal distribution)
    """
    return returns.kurtosis()


def calmar(returns: PandasDataType) -> PandasDataType:
    """ calculates the calmar ratio (CAGR% / MaxDD%) """
    return cagr(returns) / abs(max_drawdown(returns))


def ulcer_index(returns: PandasDataType) -> PandasDataType:
    """ calculates the ulcer index score (downside risk measurment) """
    dd = 1.0 - returns / returns.cummax()
    return sqrt(divide((dd ** 2).sum(), returns.shape[0] - 1))


def ulcer_performance_index(returns: PandasDataType) -> PandasDataType:
    """
    calculates the ulcer index score
    (downside risk measurment)
    """
    dd = 1.0 - returns / returns.cummax()
    ulcer = sqrt(divide((dd ** 2).sum(), returns.shape[0] - 1))
    return returns.mean() / ulcer


def risk_of_ruin(returns: PandasDataType) -> PandasDataType:
    """
    calculates the risk of ruin
    (the likelihood of losing all one's investment capital)
    """
    wins = win_rate(returns)
    return ((1 - wins) / (1 + wins)) ** len(returns)


def value_at_risk(returns: PandasDataType, sigma=1, confidence=0.95) -> PandasDataType:
    """
    calculats the daily value-at-risk
    (variance-covariance calculation with confidence n)
    """
    mu = returns.mean()
    sigma *= returns.std()

    if confidence > 1:
        confidence = confidence / 100

    return norm.ppf(1 - confidence, mu, sigma)


def conditional_value_at_risk(returns: PandasDataType, sigma=1, confidence=0.95):
    """
    calculats the conditional daily value-at-risk (aka expected shortfall)
    quantifies the amount of tail risk an investment
    """

    var = value_at_risk(returns, sigma, confidence)
    c_var = returns[returns < var].values.mean()
    return c_var if ~_np.isnan(c_var) else var


def expected_shortfall(returns, sigma=1, confidence=0.95):
    """ shorthand for conditional_value_at_risk() """
    return conditional_value_at_risk(returns, sigma, confidence)


def tail_ratio(returns: PandasDataType, cutoff=0.95) -> PandasDataType:
    """
    measures the ratio between the right
    (95%) and left tail (5%).
    """
    return abs(returns.quantile(cutoff) / returns.quantile(1 - cutoff))


def payoff_ratio(returns: PandasDataType) -> PandasDataType:
    """ measures the payoff ratio (average win/average loss) """
    return avg_win(returns) / abs(avg_loss(returns))


def win_loss_ratio(returns):
    """ shorthand for payoff_ratio() """
    return payoff_ratio(returns)


def profit_ratio(returns: PandasDataType) -> PandasDataType:
    """ measures the profit ratio (win ratio / loss ratio) """

    wins = returns[returns >= 0]
    loss = returns[returns < 0]

    win_ratio = abs(wins.mean() / wins.count())
    loss_ratio = abs(loss.mean() / loss.count())
    try:
        return win_ratio / loss_ratio
    except ZeroDivisionError:
        return 0.0


def profit_factor(returns: PandasDataType) -> PandasDataType:
    """ measures the profit ratio (wins/loss) """
    return abs(returns[returns >= 0].sum() / returns[returns < 0].sum())


def cpc_index(returns: PandasDataType) -> PandasDataType:
    """
    measures the cpc ratio
    (profit factor * win % * win loss ratio)
    """
    return profit_factor(returns) * win_rate(returns) * win_loss_ratio(returns)


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


def recovery_factor(returns: PandasDataType) -> PandasDataType:
    """ measures how fast the strategy recovers from drawdowns """
    total_returns = comp(returns)
    max_dd = max_drawdown(returns)
    return total_returns / abs(max_dd)


def max_drawdown(values: PandasDataType) -> PandasDataType:
    """ calculates the maximum drawdown """
    return (values / values.expanding(min_periods=0).max()).min() - 1


def to_drawdown_series(values: PandasDataType) -> PandasDataType:
    """ convert price series to drawdown series """
    dd = values / maximum.accumulate(values) - 1.0
    return dd.replace([Inf, -Inf, -0], 0)


def drawdown_details(drawdown):
    """
    calculates drawdown details, including start/end/valley dates,
    duration, max drawdown and max dd for 99% of the dd period
    for every drawdown period
    """

    def _drawdown_details(drawdown):
        # mark no drawdown
        no_dd = drawdown == 0

        # extract dd start dates
        starts = ~no_dd & no_dd.shift(1)
        starts = list(starts[starts].index)

        # extract end dates
        ends = no_dd & (~no_dd).shift(1)
        ends = list(ends[ends].index)

        # no drawdown :)
        if not starts:
            return DataFrame(
                index=[],
                columns=(
                    "start",
                    "valley",
                    "end",
                    "days",
                    "max drawdown",
                    "99% max drawdown",
                ),
            )

        # drawdown series begins in a drawdown
        if ends and starts[0] > ends[0]:
            starts.insert(0, drawdown.index[0])

        # series ends in a drawdown fill with last date
        if not ends or starts[-1] > ends[-1]:
            ends.append(drawdown.index[-1])

        # build dataframe from results
        data = []
        for i, _ in enumerate(starts):
            dd = drawdown[starts[i] : ends[i]]
            clean_dd = -remove_outliers(-dd, 0.99)
            data.append(
                (
                    starts[i],
                    dd.idxmin(),
                    ends[i],
                    (ends[i] - starts[i]).days,
                    dd.min() * 100,
                    clean_dd.min() * 100,
                )
            )

        df = DataFrame(
            data=data,
            columns=(
                "start",
                "valley",
                "end",
                "days",
                "max drawdown",
                "99% max drawdown",
            ),
        )
        df["days"] = df["days"].astype(int)
        df["max drawdown"] = df["max drawdown"].astype(float)
        df["99% max drawdown"] = df["99% max drawdown"].astype(float)

        df["start"] = df["start"].dt.strftime("%Y-%m-%d")
        df["end"] = df["end"].dt.strftime("%Y-%m-%d")
        df["valley"] = df["valley"].dt.strftime("%Y-%m-%d")

        return df

    if isinstance(drawdown, DataFrame):
        _dfs = {}
        for col in drawdown.columns:
            _dfs[col] = _drawdown_details(drawdown[col])
        return concat(_dfs, axis=1)

    return _drawdown_details(drawdown)


def kelly_criterion(returns):
    """
    calculates the recommended maximum amount of capital that
    should be allocated to the given strategy, based on the
    Kelly Criterion (http://en.wikipedia.org/wiki/Kelly_criterion)
    """
    win_loss_ratio = payoff_ratio(returns)
    win_prob = win_rate(returns)
    lose_prob = 1 - win_prob

    return ((win_loss_ratio * win_prob) - lose_prob) / win_loss_ratio


# ==== VS. BENCHMARK ====


def r_squared(returns: PandasDataType, benchmark: Series):
    """Measures the straight line fit of the equity curve """
    _, _, r_val, _, _ = linregress(returns, benchmark)
    return r_val ** 2


def information_ratio(returns: PandasDataType, benchmark: Series) -> PandasDataType:
    """
    calculates the information ratio
    (basically the risk return ratio of the net profits)
    """
    diff_rets = returns - benchmark
    return diff_rets.mean() / diff_rets.std()


def greeks(returns: PandasDataType, benchmark: Series, periods=252.0) -> Series:
    """ calculates alpha and beta of the portfolio """

    # find covariance
    matrix = cov(returns, benchmark)
    beta = matrix[0, 1] / matrix[1, 1]

    # calculates measures now
    alpha = returns.mean() - beta * benchmark.mean()
    alpha = alpha * periods

    # vol
    vol = volatility(matrix[0, 0])

    return Series({"beta": beta, "alpha": alpha, "vol": vol}).fillna(0)


def rolling_greeks(returns: PandasDataType, benchmark: Series, periods=252):
    """ calculates rolling alpha and beta of the portfolio """
    df = DataFrame(data={"returns": returns, "benchmark": benchmark})
    df = df.fillna(0)
    corr = df.rolling(int(periods)).corr().unstack()["returns"]["benchmark"]
    std = df.rolling(int(periods)).std()
    beta = corr * std["returns"] / std["benchmark"]
    alpha = df["returns"].mean() - beta * df["benchmark"].mean()
    # alpha = alpha * periods
    return DataFrame(index=returns.index, data={"beta": beta, "alpha": alpha}).fillna(0)
