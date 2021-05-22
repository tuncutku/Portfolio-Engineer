"""Test basic objects"""
# pylint: disable=pointless-statement, unused-argument, no-self-use


import pytest

from src.market import SingleValue, IndexValue
from src.market.ref_data import usd_ccy, cad_ccy
from tests.test_data import market
from tests.test_data import environment


def test_value(mock_symbol):
    """Test basic value."""

    assert str(market.aapl_single_value) == "79.27335357666016 USD"
    assert market.aapl_single_value.to(cad_ccy) == SingleValue(
        95.12802429199219, cad_ccy
    )
    assert round(market.aapl_single_value, 5) == SingleValue(79.27335, usd_ccy)


def test_value_sum():
    """Test value summation."""

    with pytest.raises(ValueError):
        market.aapl_single_value + market.ry_to_single_value

    sum_value = market.aapl_single_value + market.tsla_single_value
    sum_value_inverse = market.tsla_single_value + market.aapl_single_value

    assert sum_value == SingleValue(242.3853530883789, usd_ccy)
    assert sum_value == sum_value_inverse

    assert sum_value + 2 == SingleValue(244.3853530883789, usd_ccy)
    assert sum_value + 2 == 2 + sum_value


def test_value_multiplication():
    """Test index multiplication."""

    new_value = market.aapl_single_value * 2
    new_value_inverse = 2 * market.aapl_single_value
    assert new_value == SingleValue(158.5467071533203, usd_ccy)
    assert new_value == new_value_inverse


def test_index(mock_symbol):
    """Test basic index."""

    assert str(market.aapl_index) == "Index USD: 2020-05-04 / 2020-05-20"
    assert market.aapl_index.to(cad_ccy) == IndexValue(market.aapl_series_cad, cad_ccy)
    assert round(market.aapl_index, 5) == IndexValue(market.aapl_series_round, usd_ccy)


def test_index_sum():
    """Test index summation."""

    with pytest.raises(ValueError):
        market.aapl_index + market.ry_to_index

    sum_index = market.aapl_index + market.pbw_index
    sum_index_inverse = market.pbw_index + market.aapl_index

    assert sum_index == market.appl_pbw_sum_index
    assert sum_index == sum_index_inverse


def test_index_multiplication():
    """Test index multiplication."""

    assert market.aapl_index * 2 == 2 * market.aapl_index
    mult_index = market.aapl_index.multiply(environment.sample_quantity)
    assert mult_index == market.appl_mkt_value_index


def test_index_replace():
    """Test index replace method."""

    market.aapl_index.replace(environment.sample_cost_raw)
    assert market.aapl_index == market.aapl_replaced_index
