"""Return analytics."""

# pylint: disable=too-many-arguments

from pandas import Series, DataFrame

from src.analytics.utils import PandasDataType
from src.analytics.value_adjustments import compsum


def single_return(
    values: PandasDataType,
    period: int = 1,
    cumulative: bool = False,
    preserve_row: bool = True,
) -> PandasDataType:
    """Calculate single periodic return."""

    returns = values.pct_change(period)
    return compsum(returns, preserve_row) if cumulative else returns.iloc[1:]


def portfolio_return(
    security_values: DataFrame,
    security_quantities: DataFrame,
    name: str = "Portfolio",
    period: int = 1,
    cumulative: bool = False,
    preserve_row: bool = True,
) -> Series:
    """Calculate weighted periodic return."""

    security_returns = security_values.pct_change(period)
    position_values = security_values * security_quantities
    security_weights = position_values.div(position_values.sum(axis=1), axis=0)
    returns = (security_returns * security_weights).sum(axis=1)
    returns.rename(name, inplace=True)

    return compsum(returns, preserve_row) if cumulative else returns.iloc[1:]
