"""Return analytics."""

from datetime import date
from typing import Union
from pandas import Series, DataFrame

PandasDataType = Union[Series, DataFrame]


# def annualized_return(values: Series, quantites: Series) -> Series:
#     """Calculate annualized return.."""


def periodic_return(
    values: PandasDataType, period: int = 1, cumulative: bool = False
) -> PandasDataType:
    """Calculate single periodic return."""

    returns = values.pct_change(period)

    if cumulative:
        returns.fillna(0, inplace=True)
        returns = (1 + returns).cumprod()
    else:
        returns.dropna(inplace=True)

    return returns


def holding_period_return(
    values: PandasDataType,
    start_date: date,
    end_date: date = date.today(),
    annualized: bool = False,
):
    """Holding period return."""

    time_format = "%Y-%m-%d"

    # start_value = values[start_date.strftime(time_format)]
    start_value = values.loc[start_date.strftime(time_format)]
    end_value = values.loc[end_date.strftime(time_format)]
    # end_value = values[end_date.strftime(time_format)]
    hpr = (end_value - start_value) / start_value

    if annualized:
        _filter_values(hpr, start_date, end_date)
        #  (df['date'] > start_date) & (df['date'] <= end_date)
        # days =


def weighted_periodic_return(
    values: DataFrame,
    period: int = 1,
    cumulative: bool = False,
    name: str = "Portfolio",
) -> Series:
    """Calculate weighted periodic return."""

    periodic_returns = values.pct_change(period)
    weights = values.div(values.sum(axis=1), axis=0)
    returns = (periodic_returns * weights).sum(axis=1)

    if cumulative:
        returns = (1 + returns).cumprod()
    else:
        returns.drop(returns.index[0], axis=0, inplace=True)

    return returns.rename(name, inplace=True)


def _filter_values(values: PandasDataType, start: date, end: date) -> PandasDataType:
    """Filter values by given dates."""

    greater = values.index.date >= start
    smaller = values.index.date <= end

    return values.loc[greater & smaller]
