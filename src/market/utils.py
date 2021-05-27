"""Common utility functions used in views."""
# pylint: disable=invalid-name

from datetime import date

from pandas import Timestamp
from pandas.tseries.offsets import BDay


def get_business_day(date_input: date) -> date:
    """Get the closest business day by given date."""

    if date_input.weekday() in (5, 6):
        friday: Timestamp = date_input - BDay(1)
        date_input = friday.date()
    return date_input
