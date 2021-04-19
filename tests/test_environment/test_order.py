# pylint: disable=unused-argument

from datetime import datetime
from pandas import DataFrame

from tests.sample_data import order_1_2
from tests.utils import create_user, create_portfolio, create_position, create_order

from src.environment.order import Order, OrderSideType


def test_order_object(client, _db, test_data):
    """Integration test for orders."""

    # Create order
    assert Order.find_by_id(2) is None
    order = Order(**order_1_2, position=test_data.position)
    order.save_to_db()
    assert Order.find_by_id(2) is not None

    # Check basic attributes
    assert order.id == 2
    assert order.quantity == 2
    assert order.direction == OrderSideType.Sell
    assert order.price == 11
    assert isinstance(order.time, datetime)
    assert order.fee == 0
    assert repr(order) == "<Order quantity: 2, direction: Sell.>"

    # Delete order
    order.delete_from_db()
    assert Order.find_by_id(2) is None


def test_order_methods(client, _db, test_data):
    """Unit test for additional order attributes."""

    order = Order(**order_1_2, position=test_data.position)
    order.save_to_db()

    assert test_data.order.adjusted_quantity == 10
    assert order.adjusted_quantity == -2

    # Edit Order
    order.edit(20, OrderSideType.Buy, 100, datetime(2020, 1, 1), 10)
    assert order.quantity == 20
    assert order.direction == OrderSideType.Buy
    assert order.price == 100
    assert order.time == datetime(2020, 1, 1)
    assert order.fee == 10

    # Test df
    order_df = DataFrame(
        data=[[20, 100.0, 10.0]],
        index=[datetime(2020, 1, 1, 0, 0)],
        columns=["Quantity", "Quote", "Fee"],
    )
    assert order_df.equals(order.to_df())
