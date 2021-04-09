from tests.sample_data import *
from tests.utils import create_user, create_portfolio, create_position, create_order

from src.environment.order import Order


def test_order_basics(client, db):
    """Integration test for orders."""

    user = create_user(**user_1)
    port = create_portfolio(**portfolio_1, user=user)
    pos = create_position(**position_1, portfolio=port)

    # Create order
    assert Order.query.filter_by(position=pos).first() is None
    order = create_order(**order_1, position=pos)
    assert Order.query.filter_by(position=pos).all() is not None
    assert Order.find_by_id(1) != None

    # Check basic attributes
    assert order.id == 1
    assert order.symbol == "AAPL"
    assert order.quantity == 10
    assert order.side == OrderSideType.Buy
    assert order.exec_price == 10.5
    assert isinstance(order.exec_time, datetime)
    assert order.fee == 0.123
    assert repr(order) == "<Order AAPL.>"

    # Delete order
    order.delete_from_db()
    assert Order.query.filter_by(position=pos).first() is None


def test_order_attributes(client, db):
    """Unit test for additional order attributes."""

    user = create_user(**user_1)
    port = create_portfolio(**portfolio_1, user=user)
    pos = create_position(**position_1, portfolio=port)
    order_buy = create_order(**order_1, position=pos)
    order_sell = create_order(**order_2, position=pos)

    assert order_buy.adjusted_quantity == 10
    assert order_sell.adjusted_quantity == -2

    # Edit Order
    order_buy.edit("FB", 20, OrderSideType.Sell, 100, datetime(2020, 1, 1), 10)
    assert order_buy.symbol == "FB"
    assert order_buy.quantity == 20
    assert order_buy.side == OrderSideType.Sell
    assert order_buy.exec_price == 100
    assert order_buy.exec_time == datetime(2020, 1, 1)
    assert order_buy.fee == 10
