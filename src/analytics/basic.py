"""Utility analytics functions."""

# __all__ = ["mtd", "qtd"]

from datetime import datetime
from math import ceil

from numpy import isnan, sqrt
from pandas import Series, DataFrame

from src.analytics.utils import Period, PandasDataType


def mtd(data: PandasDataType) -> PandasDataType:
    """Filter given data to month to date."""
    return data[data.index >= datetime.now().strftime("%Y-%m-01")]


def qtd(data: PandasDataType) -> PandasDataType:
    """Filter given data to quarter to date."""
    date = datetime.now()
    for quarter in [1, 4, 7, 10]:
        if date.month <= quarter:
            return data[
                data.index >= datetime(date.year, quarter, 1).strftime("%Y-%m-01")
            ]
    return data[data.index >= date.strftime("%Y-%m-01")]


def ytd(data: PandasDataType) -> PandasDataType:
    """Filter given data to year to date."""
    return data[data.index >= datetime.now().strftime("%Y-01-01")]


def get_outliers(data: PandasDataType, quantile=0.95) -> PandasDataType:
    """Return values of outliers """
    return data[data > data.quantile(quantile)].dropna(how="all")


def remove_outliers(data: PandasDataType, quantile=0.95) -> PandasDataType:
    """Returns values without outliers """
    return data[data < data.quantile(quantile)].dropna(how="all")


def compsum(returns: PandasDataType) -> PandasDataType:
    """ Calculates rolling compounded returns """
    return returns.add(1).cumprod().add(-1)


def comp(returns: PandasDataType) -> Series:
    """ Calculates total compounded returns """
    return returns.add(1).prod() - 1


def aggregate_values(
    returns: PandasDataType, period: Period = Period.daily
) -> PandasDataType:
    """ Aggregates returns based on date periods."""
    return returns.resample(period.value).last()


def aggregate_returns(
    returns: PandasDataType, period: Period = Period.daily
) -> PandasDataType:
    """ Aggregates returns based on date periods."""
    return returns.resample(period.value).apply(comp)


# TODO: display dates as well.
def _count_consecutive(data: PandasDataType) -> PandasDataType:
    """Counts consecutive dates (like cumsum() with reset on zeroes)."""

    def _count(data: Series):
        return data * (data.groupby((data != data.shift(1)).cumsum()).cumcount() + 1)

    if isinstance(data, DataFrame):
        for col in data.columns:
            data[col] = _count(data[col])
        return data
    return _count(data)


def consecutive_wins(returns: PandasDataType) -> PandasDataType:
    """Returns the maximum consecutive wins."""
    return _count_consecutive(returns > 0).max()


def consecutive_losses(returns: PandasDataType) -> PandasDataType:
    """Returns the maximum consecutive losses."""
    return _count_consecutive(returns < 0).max()


def exposure(returns: PandasDataType) -> PandasDataType:
    """Returns the market exposure time (returns != 0)."""

    def _exposure(ret: Series):
        ex = len(ret[(~isnan(ret)) & (ret != 0)]) / len(ret)
        return ceil(ex * 100) / 100

    if isinstance(returns, DataFrame):
        _df = {}
        for col in returns.columns:
            _df[col] = _exposure(returns[col])
        return Series(_df)
    return _exposure(returns)


def win_rate(returns: PandasDataType) -> PandasDataType:
    """Calculates the win ratio for a period."""

    def _win_rate(ret: Series):
        try:
            return round(len(ret[ret > 0]) / len(ret[ret != 0]), 5)
        except ZeroDivisionError:
            return 0.0

    if isinstance(returns, DataFrame):
        _df = {}
        for col in returns.columns:
            _df[col] = _win_rate(returns[col])
        return Series(_df)
    return _win_rate(returns)


def avg_return(returns: PandasDataType) -> PandasDataType:
    """Calculates the average return/trade return for a period."""
    return round(returns[returns != 0].dropna().mean(), 5)


def avg_win(returns: PandasDataType) -> PandasDataType:
    """Calculates the average winning return/trade return for a period."""
    return round(returns[returns > 0].dropna().mean(), 5)


def avg_loss(returns: PandasDataType) -> PandasDataType:
    """Calculates the average low if return/trade return for a period."""
    return round(returns[returns < 0].dropna().mean(), 5)


def volatility(
    returns: PandasDataType, annualize: bool = True, trading_year_days=252
) -> PandasDataType:
    """Calculates the volatility of daily returns."""
    std = returns.std()
    if annualize:
        return round(std * sqrt(trading_year_days), 5)
    return round(std, 5)
