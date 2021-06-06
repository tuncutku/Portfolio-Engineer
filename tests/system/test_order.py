"""Test order endpoints"""
# pylint: disable=unused-argument

from datetime import datetime

from src.environment.position import Position
from src.environment.order import Order, OrderSideType
from src.forms.order import date_time_format
from src.market import Instrument, SingleValue
from src.market.ref_data import usd_ccy

from tests.system.common import templete_used


def test_add_order(client, _db, load_environment_data, login, captured_templates):
    """System test for add order endpoint."""

    response = client.get("order/1/add_order", follow_redirects=True)
    assert response.status_code == 200
    assert "Add new order" in response.get_data(as_text=True)

    # Test to post an order that has a position.
    response = client.post(
        "order/1/add_order",
        data=dict(
            symbol="FB",
            quantity=6,
            direction=OrderSideType.Sell,
            cost=10,
            exec_datetime=datetime(2020, 1, 2).strftime(date_time_format),
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200

    new_order = Order.find_by_id(7)
    assert new_order.quantity == 6
    assert new_order.direction == OrderSideType.Sell
    assert new_order.cost == SingleValue(10, usd_ccy)
    assert new_order.time == datetime(2020, 1, 2)

    new_pos = Position.find_by_id(3)
    assert new_pos
    assert isinstance(new_pos.security, Instrument)

    template_list = ["order/add_order.html", "portfolio/list_portfolios.html"]
    templete_used(template_list, captured_templates)


def test_edit_order(client, _db, load_environment_data, login, captured_templates):
    """System test for edit order endpoint."""

    response = client.get("order/edit/1", follow_redirects=True)
    assert response.status_code == 200
    assert "Edit order:" in response.get_data(as_text=True)
    assert "AAPL" in response.get_data(as_text=True)
    assert "10" in response.get_data(as_text=True)
    assert "130" in response.get_data(as_text=True)
    assert "2020-02-03" in response.get_data(as_text=True)
    assert "Buy" in response.get_data(as_text=True)

    response = client.post(
        "order/edit/1",
        data=dict(
            symbol="AAPL",
            quantity=10,
            direction=OrderSideType.Buy,
            cost=101,
            exec_datetime=datetime(2019, 1, 3).strftime(date_time_format),
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200

    order_test = Order.find_by_id(1)
    assert order_test.quantity == 10
    assert order_test.direction == OrderSideType.Buy
    assert order_test.cost == SingleValue(101, usd_ccy)
    assert order_test.time == datetime(2019, 1, 3)

    template_list = ["order/edit_order.html", "portfolio/list_portfolios.html"]
    templete_used(template_list, captured_templates)


def test_delete_order(client, _db, captured_templates, load_environment_data, login):
    """System test for delete order endpoint."""

    assert Order.find_by_id(1) is not None
    response = client.get("order/delete_order/1", follow_redirects=True)
    assert response.status_code == 200
    assert Order.find_by_id(1) is None

    template_list = ["portfolio/list_portfolios.html"]
    templete_used(template_list, captured_templates)
