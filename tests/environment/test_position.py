"""Test position object"""
# pylint: disable=unused-argument

from datetime import date
from pandas import Series

from src.environment import Position
from src.market import SingleValue
from src.market.ref_data import usd_ccy, cad_ccy

from tests.test_data import environment as env

start_date = date(2020, 1, 1)
end_date = date(2021, 1, 1)


def test_position_object(client, _db, load_environment_data):
    """Test saved position object."""

    position = Position.find_by_id(1)

    assert position == Position.find_by_id(1)
    assert position.id == 1
    assert position.security == env.position_1_raw["security"]
    assert repr(position) == "<Position AAPL.>"


def test_position_quantity(client, _db, load_environment_data):
    """Test position quantities."""

    position = Position.find_by_id(1)
    assert position.open_quantity == 22
    assert position.is_open
    quantity = position.quantity
    assert quantity.equals(env.position_1_quantity)
    cum_quantity = position.cumulative_quantity_index
    assert isinstance(cum_quantity, Series)


def test_position_cost(client, _db, load_environment_data):
    """Test position cost."""

    position = Position.find_by_id(1)
    cost = position.cost
    assert cost.equals(env.position_1_cost)


def test_position_values(client, _db, load_environment_data, mock_symbol):
    """Unit test for position values."""

    position = Position.find_by_id(1)

    # Test current value
    assert position.current_value() == SingleValue(2640, usd_ccy)
    assert position.current_value(cad_ccy) == SingleValue(3168.0, cad_ccy)

    # Test position historical value
    position_hist_value = position.historical_value(start_date, end_date)
    assert position_hist_value == env.position_1_values_index