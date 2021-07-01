"""Metrics"""

from scipy.stats import linregress

# ======= Basic Metrics =======


def sharpe(returns, rf=0.0, periods=252, annualize=True, trading_year_days=252):
    """
    calculates the sharpe ratio of access returns

    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms

    Args:
        * returns (Series, DataFrame): Input return series
        * rf (float): Risk-free rate expressed as a yearly (annualized) return
        * periods (int): Freq. of returns (252/365 for daily, 12 for monthly)
        * annualize: return annualize sharpe?
    """

    if rf != 0 and periods is None:
        raise Exception("Must provide periods if rf != 0")

    returns = _utils._prepare_returns(returns, rf, periods)
    res = returns.mean() / returns.std()

    if annualize:
        return res * _np.sqrt(1 if trading_year_days is None else trading_year_days)

    return res


def sortino(returns, rf=0, periods=252, annualize=True, trading_year_days=252):
    """
    calculates the sortino ratio of access returns

    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms

    Calculation is based on this paper by Red Rock Capital
    http://www.redrockcapital.com/Sortino__A__Sharper__Ratio_Red_Rock_Capital.pdf
    """

    if rf != 0 and periods is None:
        raise Exception("Must provide periods if rf != 0")

    returns = _utils._prepare_returns(returns, rf, periods)

    downside = (returns[returns < 0] ** 2).sum() / len(returns)
    res = returns.mean() / _np.sqrt(downside)

    if annualize:
        return res * _np.sqrt(1 if trading_year_days is None else trading_year_days)

    return res


def adjusted_sortino(returns, rf=0, periods=252, annualize=True, trading_year_days=252):
    """
    Jack Schwager's version of the Sortino ratio allows for
    direct comparisons to the Sharpe. See here for more info:
    https://archive.is/wip/2rwFW
    """
    data = sortino(
        returns,
        rf=0,
        periods=periods,
        annualize=annualize,
        trading_year_days=trading_year_days,
    )
    return data / _sqrt(2)


def gain_to_pain_ratio(returns, rf=0, resolution="D"):
    """
    Jack Schwager's GPR. See here for more info:
    https://archive.is/wip/2rwFW
    """
    returns = _utils._prepare_returns(returns, rf).resample(resolution).sum()
    downside = abs(returns[returns < 0].sum())
    return returns.sum() / downside


def cagr(returns, rf=0.0, compounded=True):
    """
    calculates the communicative annualized growth return
    (CAGR%) of access returns

    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms
    """

    total = _utils._prepare_returns(returns, rf)
    if compounded:
        total = comp(total)
    else:
        total = _np.sum(total)

    years = (returns.index[-1] - returns.index[0]).days / 365.0

    res = abs(total + 1.0) ** (1.0 / years) - 1

    if isinstance(returns, _pd.DataFrame):
        res = _pd.Series(res)
        res.index = returns.columns

    return res


def rar(returns, rf=0.0):
    """
    calculates the risk-adjusted return of access returns
    (CAGR / exposure. takes time into account.)

    If rf is non-zero, you must specify periods.
    In this case, rf is assumed to be expressed in yearly (annualized) terms
    """
    returns = _utils._prepare_returns(returns, rf)
    return cagr(returns) / exposure(returns)


def skew(returns):
    """
    calculates returns' skewness
    (the degree of asymmetry of a distribution around its mean)
    """
    return _utils._prepare_returns(returns).skew()


def kurtosis(returns):
    """
    calculates returns' kurtosis
    (the degree to which a distribution peak compared to a normal distribution)
    """
    return _utils._prepare_returns(returns).kurtosis()


def calmar(returns):
    """ calculates the calmar ratio (CAGR% / MaxDD%) """
    returns = _utils._prepare_returns(returns)
    cagr_ratio = cagr(returns)
    max_dd = max_drawdown(returns)
    return cagr_ratio / abs(max_dd)


def ulcer_index(returns, rf=0):
    """ calculates the ulcer index score (downside risk measurment) """
    returns = _utils._prepare_returns(returns, rf)
    dd = 1.0 - returns / returns.cummax()
    return _np.sqrt(_np.divide((dd ** 2).sum(), returns.shape[0] - 1))


def ulcer_performance_index(returns, rf=0):
    """
    calculates the ulcer index score
    (downside risk measurment)
    """
    returns = _utils._prepare_returns(returns, rf)
    dd = 1.0 - returns / returns.cummax()
    ulcer = _np.sqrt(_np.divide((dd ** 2).sum(), returns.shape[0] - 1))
    return returns.mean() / ulcer


def upi(returns, rf=0):
    """ shorthand for ulcer_performance_index() """
    return ulcer_performance_index(returns, rf)


def risk_of_ruin(returns):
    """
    calculates the risk of ruin
    (the likelihood of losing all one's investment capital)
    """
    returns = _utils._prepare_returns(returns)
    wins = win_rate(returns)
    return ((1 - wins) / (1 + wins)) ** len(returns)


def ror(returns):
    """ shorthand for risk_of_ruin() """
    return risk_of_ruin(returns)


def value_at_risk(returns, sigma=1, confidence=0.95):
    """
    calculats the daily value-at-risk
    (variance-covariance calculation with confidence n)
    """
    returns = _utils._prepare_returns(returns)
    mu = returns.mean()
    sigma *= returns.std()

    if confidence > 1:
        confidence = confidence / 100

    return _norm.ppf(1 - confidence, mu, sigma)


def var(returns, sigma=1, confidence=0.95):
    """ shorthand for value_at_risk() """
    return value_at_risk(returns, sigma, confidence)


def conditional_value_at_risk(returns, sigma=1, confidence=0.95):
    """
    calculats the conditional daily value-at-risk (aka expected shortfall)
    quantifies the amount of tail risk an investment
    """
    returns = _utils._prepare_returns(returns)
    var = value_at_risk(returns, sigma, confidence)
    c_var = returns[returns < var].values.mean()
    return c_var if ~_np.isnan(c_var) else var


def cvar(returns, sigma=1, confidence=0.95):
    """ shorthand for conditional_value_at_risk() """
    return conditional_value_at_risk(returns, sigma, confidence)


def expected_shortfall(returns, sigma=1, confidence=0.95):
    """ shorthand for conditional_value_at_risk() """
    return conditional_value_at_risk(returns, sigma, confidence)


def tail_ratio(returns, cutoff=0.95):
    """
    measures the ratio between the right
    (95%) and left tail (5%).
    """
    returns = _utils._prepare_returns(returns)
    return abs(returns.quantile(cutoff) / returns.quantile(1 - cutoff))


def payoff_ratio(returns):
    """ measures the payoff ratio (average win/average loss) """
    returns = _utils._prepare_returns(returns)
    return avg_win(returns) / abs(avg_loss(returns))


def win_loss_ratio(returns):
    """ shorthand for payoff_ratio() """
    return payoff_ratio(returns)


def profit_ratio(returns):
    """ measures the profit ratio (win ratio / loss ratio) """
    returns = _utils._prepare_returns(returns)
    wins = returns[returns >= 0]
    loss = returns[returns < 0]

    win_ratio = abs(wins.mean() / wins.count())
    loss_ratio = abs(loss.mean() / loss.count())
    try:
        return win_ratio / loss_ratio
    except Exception:
        return 0.0


def profit_factor(returns):
    """ measures the profit ratio (wins/loss) """
    returns = _utils._prepare_returns(returns)
    return abs(returns[returns >= 0].sum() / returns[returns < 0].sum())


def cpc_index(returns):
    """
    measures the cpc ratio
    (profit factor * win % * win loss ratio)
    """
    returns = _utils._prepare_returns(returns)
    return profit_factor(returns) * win_rate(returns) * win_loss_ratio(returns)


def common_sense_ratio(returns):
    """ measures the common sense ratio (profit factor * tail ratio) """
    returns = _utils._prepare_returns(returns)
    return profit_factor(returns) * tail_ratio(returns)


def outlier_win_ratio(returns, quantile=0.99):
    """
    calculates the outlier winners ratio
    99th percentile of returns / mean positive return
    """
    returns = _utils._prepare_returns(returns)
    return returns.quantile(quantile).mean() / returns[returns >= 0].mean()


def outlier_loss_ratio(returns, quantile=0.01):
    """
    calculates the outlier losers ratio
    1st percentile of returns / mean negative return
    """
    returns = _utils._prepare_returns(returns)
    return returns.quantile(quantile).mean() / returns[returns < 0].mean()


def recovery_factor(returns):
    """ measures how fast the strategy recovers from drawdowns """
    returns = _utils._prepare_returns(returns)
    total_returns = comp(returns)
    max_dd = max_drawdown(returns)
    return total_returns / abs(max_dd)


def risk_return_ratio(returns):
    """
    calculates the return / risk ratio
    (sharpe ratio without factoring in the risk-free rate)
    """
    returns = _utils._prepare_returns(returns)
    return returns.mean() / returns.std()


def max_drawdown(prices):
    """ calculates the maximum drawdown """
    prices = _utils._prepare_prices(prices)
    return (prices / prices.expanding(min_periods=0).max()).min() - 1


def to_drawdown_series(prices):
    """ convert price series to drawdown series """
    prices = _utils._prepare_prices(prices)
    dd = prices / _np.maximum.accumulate(prices) - 1.0
    return dd.replace([_np.inf, -_np.inf, -0], 0)


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
            return _pd.DataFrame(
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

        df = _pd.DataFrame(
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

    if isinstance(drawdown, _pd.DataFrame):
        _dfs = {}
        for col in drawdown.columns:
            _dfs[col] = _drawdown_details(drawdown[col])
        return _pd.concat(_dfs, axis=1)

    return _drawdown_details(drawdown)


def kelly_criterion(returns):
    """
    calculates the recommended maximum amount of capital that
    should be allocated to the given strategy, based on the
    Kelly Criterion (http://en.wikipedia.org/wiki/Kelly_criterion)
    """
    returns = _utils._prepare_returns(returns)
    win_loss_ratio = payoff_ratio(returns)
    win_prob = win_rate(returns)
    lose_prob = 1 - win_prob

    return ((win_loss_ratio * win_prob) - lose_prob) / win_loss_ratio


# ==== VS. BENCHMARK ====


def r_squared(values, benchmark):
    """ measures the straight line fit of the equity curve """
    _, _, r_val, _, _ = linregress(
        _utils._prepare_returns(returns),
        _utils._prepare_benchmark(benchmark, returns.index),
    )
    return r_val ** 2


def r2(returns, benchmark):
    """ shorthand for r_squared() """
    return r_squared(returns, benchmark)


def information_ratio(returns, benchmark):
    """
    calculates the information ratio
    (basically the risk return ratio of the net profits)
    """
    diff_rets = _utils._prepare_returns(returns) - _utils._prepare_benchmark(
        benchmark, returns.index
    )

    return diff_rets.mean() / diff_rets.std()


def greeks(returns, benchmark, periods=252.0):
    """ calculates alpha and beta of the portfolio """

    # find covariance
    matrix = _np.cov(returns, benchmark)
    beta = matrix[0, 1] / matrix[1, 1]

    # calculates measures now
    alpha = returns.mean() - beta * benchmark.mean()
    alpha = alpha * periods

    return _pd.Series(
        {
            "beta": beta,
            "alpha": alpha,
            # "vol": _np.sqrt(matrix[0, 0]) * _np.sqrt(periods)
        }
    ).fillna(0)


def rolling_greeks(returns, benchmark, periods=252):
    """ calculates rolling alpha and beta of the portfolio """
    df = _pd.DataFrame(
        data={
            "returns": _utils._prepare_returns(returns),
            "benchmark": _utils._prepare_benchmark(benchmark, returns.index),
        }
    )
    df = df.fillna(0)
    corr = df.rolling(int(periods)).corr().unstack()["returns"]["benchmark"]
    std = df.rolling(int(periods)).std()
    beta = corr * std["returns"] / std["benchmark"]

    alpha = df["returns"].mean() - beta * df["benchmark"].mean()

    # alpha = alpha * periods
    return _pd.DataFrame(
        index=returns.index, data={"beta": beta, "alpha": alpha}
    ).fillna(0)
