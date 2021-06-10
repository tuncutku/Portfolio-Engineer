"""Test position object"""
# pylint: disable=unused-argument

from datetime import date
from pandas import Series

from src.environment import Position
from src.market import SingleValue
from src.market.ref_data import usd_ccy, cad_ccy

from tests.test_data import environment as env

start_date = date(2020, 5, 4)
end_date = date(2020, 5, 20)


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
    cum_quantity_with_dates = position.cumulative_quantity_index(
        date(2020, 1, 4), date(2021, 5, 23)
    )
    assert cum_quantity_with_dates.equals(env.position_1_cum_quantity)


def test_position_cost(client, _db, load_environment_data):
    """Test position cost."""

    position = Position.find_by_id(1)
    cost = position.cost
    assert cost.equals(env.position_1_cost)


def test_position_values(client, _db, load_environment_data, mock_current_md):
    """Unit test for position values."""

    position = Position.find_by_id(1)

    # Test current value
    usd_value = position.current_value()
    cad_value = position.current_value(cad_ccy)
    assert cad_value.value > usd_value.value

    # Test position historical value
    position_hist_value = position.historical_value(start_date, end_date)
    assert position_hist_value == env.position_1_values_index
    position_hist_cad_value = position.historical_value(start_date, end_date, cad_ccy)
    assert position_hist_cad_value == env.position_1_values_cad_index