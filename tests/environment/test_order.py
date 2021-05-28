"""Test order object"""
# pylint: disable=unused-argument


from datetime import datetime, date
from pandas import Series

from src.environment import User, Order
from src.market.types import OrderSideType

from tests.test_data import environment as env


def test_order_object(client, _db, load_environment_data):
    """Test saved order object."""

    order = Order.find_by_id(1)

    assert order.id == 1
    assert order.quantity == env.order_1_raw["quantity"]
    assert order.direction == env.order_1_raw["direction"]
    assert order.cost == env.order_1_raw["cost"]
    assert isinstance(order.time, datetime)
    assert repr(order) == "<Order quantity: 10, direction: Buy.>"


def test_order_methods(client, _db, load_environment_data):
    """Unit test for order methods."""

    order = Order.find_by_id(2)

    assert order.adjusted_quantity == -2
    assert Series.equals(order.cost_df, Series([122.0], index=[date(2020, 7, 1)]))
    assert Series.equals(order.quantity_df, Series([-2], index=[date(2020, 7, 1)]))

    # Edit Order
    order.edit(20, OrderSideType.Buy, 100, datetime(2020, 1, 1))
    assert order.quantity == 20
    assert order.direction == OrderSideType.Buy
    assert order.cost == 100
    assert order.time == datetime(2020, 1, 1)
