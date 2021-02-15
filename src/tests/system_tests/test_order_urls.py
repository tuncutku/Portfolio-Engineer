from datetime import datetime
from flask_login import current_user

from src.tests.utils.base import BaseTest
from src.environment.user_activities.user import User
from src.environment.user_activities.portfolio import Portfolio, PortfolioType, Currency
from src.environment.user_activities.position import Position
from src.environment.user_activities.order import Order, OrderSideType

from src.forms.order_forms import date_time_format

a = 1


class TestOrderURLs(BaseTest):
    def test_add_order(self):

        self.login_user()

        response = self.client.get(
            "order/1/add_order",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Add new order:" in response.get_data(as_text=True))

        response = self.client.post(
            "order/1/add_order",
            data=dict(
                symbol="FB",
                quantity=6,
                side=OrderSideType.Sell,
                fee=10,
                exec_datetime=datetime(2020, 1, 1, 3, 10).strftime(date_time_format),
                price=100,
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")

        new_order = Order.find_by_id(2)
        self.assertEqual(new_order.symbol, "FB")
        self.assertEqual(new_order.quantity, 6)
        self.assertEqual(new_order.side, OrderSideType.Sell)
        self.assertEqual(new_order.fee, 10)
        self.assertEqual(new_order.exec_time, datetime(2020, 1, 1, 3, 10))
        self.assertEqual(new_order.avg_exec_price, 100)

    def test_add_order_form(self):
        pass

    def test_edit_order(self):

        self.login_user()

        response = self.client.get(
            "order/edit/1",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("order/edit_order.html")
        self.assertTrue("Edit order:" in response.get_data(as_text=True))
        self.assertTrue("AAPL" in response.get_data(as_text=True))
        self.assertTrue("10" in response.get_data(as_text=True))
        self.assertTrue("Buy" in response.get_data(as_text=True))
        self.assertTrue("10.5" in response.get_data(as_text=True))
        self.assertTrue("0.123" in response.get_data(as_text=True))

        response = self.client.post(
            "order/edit/1",
            data=dict(
                symbol="AAPL",
                quantity=6,
                side=OrderSideType.Sell,
                fee=10,
                exec_datetime=datetime(2019, 1, 1, 3, 10).strftime(date_time_format),
                price=0.2,
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")
        self.assertEqual(self.order_test.symbol, "AAPL")
        self.assertEqual(self.order_test.quantity, 6)
        self.assertEqual(self.order_test.side, OrderSideType.Sell)
        self.assertEqual(self.order_test.fee, 10)
        self.assertEqual(self.order_test.exec_time, datetime(2019, 1, 1, 3, 10))
        self.assertEqual(self.order_test.avg_exec_price, 0.2)

    def test_delete_order(self):

        self.login_user()

        self.assertIsNotNone(Order.find_by_id(1))

        response = self.client.get(
            "order/delete_order/1",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")
        self.assertIsNone(Order.find_by_id(1))