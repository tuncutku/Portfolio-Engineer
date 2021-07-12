"""Utility analytics functions."""

# __all__ = ["mtd", "qtd"]

from datetime import datetime

from src.analytics.basic import comp
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


def compsum(returns: PandasDataType, preserve_row: bool = True) -> PandasDataType:
    """ Calculates cumulative compounded returns """
    returns = returns.fillna(0).add(1).cumprod().add(-1)
    return returns if preserve_row else returns.iloc[1:]
