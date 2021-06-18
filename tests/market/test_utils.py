"""Test market utils"""

from datetime import date
from src.market import get_business_day


def test_get_business_day():
    """Test get business day."""

    weekday = date(2020, 1, 3)
    weekend = date(2020, 1, 5)

    assert weekday == get_business_day(weekday)
    assert weekday == get_business_day(weekend)
