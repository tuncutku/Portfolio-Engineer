"""Test environment object relations"""
# pylint: disable=unused-argument

from datetime import date, datetime

from src.environment import User, Portfolio, Position, Order
from tests.sample_data import user_1, portfolio_1, position_1, order_1


classes = [User, Portfolio, Position, Order]


def test_relationships(client, _db, test_user):
    """Integration test for model relationships."""

    test_user.delete_from_db()
    for _object in [User, Portfolio, Position, Order]:
        assert not _object.find_all()


def test_sample_objects(client, _db, test_user):
    """Test saved test objects."""

    for _object in [User, Portfolio, Position, Order]:
        assert _object.find_all()

    # Test portfolios.
    assert test_user == User.find_by_id(1)
    assert test_user.id == 1
    assert test_user.email == user_1["email"]
    assert repr(test_user) == "<User tuncutku10@gmail.com.>"
    assert test_user.confirmed is True

    # Test portfolios.
    portfolio = test_user.portfolios[0]
    assert portfolio == Portfolio.find_by_id(1)
    assert portfolio.id == 1
    assert portfolio.name == portfolio_1["name"]
    assert portfolio.portfolio_type == portfolio_1["portfolio_type"]
    assert portfolio.reporting_currency == portfolio_1["reporting_currency"]
    assert portfolio.benchmark == portfolio_1["benchmark"]
    assert not portfolio.primary
    assert isinstance(portfolio.date, date)
    assert repr(portfolio) == "<Portfolio portfolio_1.>"

    # Test positions.
    position = portfolio.positions[0]
    assert position == Position.find_by_id(1)
    assert position.id == 1
    assert position.security == position_1["security"]
    assert repr(position) == "<Position asset_currency=USD symbol=AAPL.>"

    # Test orders.
    order = position.orders[0]
    assert order == Order.find_by_id(1)
    assert order.id == 1
    assert order.quantity == order_1["quantity"]
    assert order.direction == order_1["direction"]
    assert order.cost == order_1["cost"]
    assert isinstance(order.time, datetime)
    assert repr(order) == "<Order quantity: 10, direction: Buy.>"

    # Test number of objects.
    assert len(User.find_all()) == 1
    assert len(Portfolio.find_all()) == 1
    assert len(Position.find_all()) == 2
    assert len(Order.find_all()) == 6
