"""Utilities for analytics"""

# pylint: disable=invalid-name

from enum import Enum
from typing import Union

from pandas import Series, DataFrame

PandasDataType = Union[Series, DataFrame]


class Period(Enum):
    """Periods used for resampling."""

    daily = "B"
    weekly = "W-FRI"
    monthly = "BM"
    yearly = "BY"
