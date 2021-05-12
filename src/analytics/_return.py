"""Return analytics."""

from typing import Union
from pandas import Series, DataFrame


# def annualized_return(values: Series, quantites: Series) -> Series:
#     """Calculate annualized return.."""


def single_periodic_return(
    values: Union[Series, DataFrame], period: int = 1, cumulative: bool = False
) -> Union[Series, DataFrame]:
    """Calculate single periodic return."""

    returns = values.pct_change(period)

    if cumulative:
        returns.fillna(0, inplace=True)
        returns = (1 + returns).cumprod()
    else:
        returns.dropna(inplace=True)

    return returns


def weighted_periodic_return(
    values: DataFrame,
    period: int = 1,
    cumulative: bool = False,
    name: str = "Portfolio",
) -> Series:
    """Calculate single periodic return."""

    periodic_returns = values.pct_change(period)
    weights = values.div(values.sum(axis=1), axis=0)
    returns = (periodic_returns * weights).sum(axis=1)

    if cumulative:
        returns = (1 + returns).cumprod()
    else:
        returns.drop(returns.index[0], axis=0, inplace=True)

    return returns.rename(name, inplace=True)
