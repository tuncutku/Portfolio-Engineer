"""Test basic objects."""
# pylint: disable=pointless-statement

import pytest
from pandas import Series, DatetimeIndex
from datetime import date

from src.market import Currency, SingleValue, IndexValue


def test_single_value():
    """Test single value."""

    value_1 = SingleValue(55, Currency("USD"))
    value_2 = SingleValue(10, Currency("USD"))

    assert value_1.value == 55
    assert value_1.currency == Currency("USD")

    new_value = value_1 + value_2

    assert isinstance(new_value, SingleValue)
    assert new_value.value == 65
    assert new_value.currency == Currency("USD")
    assert value_1 + value_2 == value_2 + value_1
    assert str(new_value) == "65 USD"

    value_3 = SingleValue(-10, Currency("CAD"))

    with pytest.raises(ValueError):
        value_1 + value_3

    new_value = new_value * 2
    assert (new_value * 2).value == (2 * new_value).value
    assert isinstance(new_value, SingleValue)
    assert new_value.value == 130
    assert new_value.currency == Currency("USD")

    value_1 = value_1.to(Currency("CAD"))
    assert value_1.currency == Currency("CAD")
    assert value_1.value != 55


def test_index_value():
    """Test index value."""

    index_1 = IndexValue(Series([10, 14, 20, 26]), Currency("USD"))
    index_2 = IndexValue(Series([20, 110, 40, 78]), Currency("USD"))

    assert Series.equals(index_1.index, Series([10, 14, 20, 26]))
    assert index_1.currency == Currency("USD")

    new_index = index_1 + index_2

    assert isinstance(new_index, IndexValue)
    assert sum(new_index.index) == 318
    assert new_index.currency == Currency("USD")

    assert Series.equals((index_1 + index_2).index, (index_2 + index_1).index)
    assert str(index_1) == "Index USD"

    index_3 = IndexValue(Series([-15, 14, -56, 16]), Currency("CAD"))

    with pytest.raises(ValueError):
        index_1 + index_3

    new_value = index_1 * 2
    assert len((index_1 * 2).index) == len((2 * index_1).index)
    assert isinstance(new_value, IndexValue)
    assert sum(new_value.index) == 140
    assert new_value.currency == Currency("USD")

    index_1 = index_1.to(Currency("CAD"))
    assert sum(index_1.index) != sum(Series([10, 14, 20, 26]))
    assert index_1.currency == Currency("CAD")


def test_currency():
    """Test currency."""

    start_date = date(2020, 1, 2)
    end_date = date(2021, 1, 4)

    usd = Currency("USD")
    date_index = usd.calender(start_date, end_date)

    assert str(usd) == "USD"
    assert isinstance(date_index, DatetimeIndex)
    assert date_index.max().date() == date(2021, 1, 4)
    assert date_index.min().date() == date(2020, 1, 2)
