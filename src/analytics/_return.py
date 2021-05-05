"""Return analytics."""
from pandas import Series


def annualized_return(values: Series, quantites: Series) -> Series:
    """Calculate annualized return.."""


def periodic_return(values: Series, period: int = 1, cumulative: bool = False):
    """Calculate periodic return."""

    returns = values.pct_change(period)
    returns.dropna(inplace=True)

    if cumulative:
        returns = (1 + returns).cumprod()

    return returns


def weighted_value():
    """Calculate weighted value."""
