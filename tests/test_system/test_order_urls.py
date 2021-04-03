from datetime import datetime

from src.environment.position import Position
from src.environment.order import Order
from src.forms.order_forms import date_time_format


from tests.sample_data import *
from tests.test_system.common import templete_used


def test_add_order(client, db, user, captured_templates, mocker):
    def mock_func(self):
        return {
            "FB": {
                "shortName": "Facebook, Inc.",
                "quoteType": "EQUITY",
                "currency": "USD",
            }
        }

    mocker.patch(
        "src.market_data.provider.YFinance.info",
        mock_func,
    )

    response = client.get("order/1/add_order", follow_redirects=True)
    assert response.status_code == 200
    assert "Add new order" in response.get_data(as_text=True)

    assert Position.find_by_id(2) == None
    # Test to post an order that has a position.
    response = client.post(
        "order/1/add_order",
        data=dict(
            symbol="FB",
            quantity=6,
            side=OrderSideType.Sell,
            fee=10,
            exec_datetime=datetime(2020, 1, 2).strftime(date_time_format),
            price=100,
        ),
        follow_redirects=True,
    )

    assert response.status_code == 200

    new_order = Order.find_by_id(2)
    assert new_order.symbol == "FB"
    assert new_order.quantity == 6
    assert new_order.side == OrderSideType.Sell
    assert new_order.fee == 10
    assert new_order.exec_time == datetime(2020, 1, 2)
    assert new_order.exec_price == 100

    new_pos = Position.find_by_id(2)
    assert new_pos != None
    assert new_pos.name == "Facebook, Inc."
    assert new_pos.security_type == "EQUITY"
    assert new_pos.currency == "USD"

    template_list = ["order/add_order.html", "portfolio/list_portfolios.html"]
    templete_used(template_list, captured_templates)


def test_edit_order(client, db, user, captured_templates):

    response = client.get("order/edit/1", follow_redirects=True)
    assert response.status_code == 200
    assert "Edit order:" in response.get_data(as_text=True)
    assert "AAPL" in response.get_data(as_text=True)
    assert "10" in response.get_data(as_text=True)
    assert "Buy" in response.get_data(as_text=True)
    assert "10.5" in response.get_data(as_text=True)
    assert "0.123" in response.get_data(as_text=True)

    response = client.post(
        "order/edit/1",
        data=dict(
            symbol="AAPL",
            quantity=6,
            side=OrderSideType.Sell,
            fee=10,
            exec_datetime=datetime(2019, 1, 2).strftime(date_time_format),
            price=0.2,
        ),
        follow_redirects=True,
    )
    assert response.status_code == 200
    order_test = Order.find_by_id(1)

    assert order_test.symbol == "AAPL"
    assert order_test.quantity == 6
    assert order_test.side == OrderSideType.Sell
    assert order_test.fee == 10
    assert order_test.exec_time == datetime(2019, 1, 2)
    assert order_test.exec_price == 0.2

    template_list = ["order/edit_order.html", "portfolio/list_portfolios.html"]
    templete_used(template_list, captured_templates)


def test_delete_order(client, db, user, captured_templates):

    assert Order.find_by_id(1) != None
    response = client.get("order/delete_order/1", follow_redirects=True)
    assert response.status_code == 200
    assert Order.find_by_id(1) == None

    template_list = ["portfolio/list_portfolios.html"]
    templete_used(template_list, captured_templates)
