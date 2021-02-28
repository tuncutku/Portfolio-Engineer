from sqlalchemy.exc import StatementError
from datetime import datetime
from unittest import mock
import pandas as pd

from src.tests.utils.base import BaseTest
from src.tests.utils.sample_data import *

from src.extensions import db
from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from src.environment.report import Report


class ModelTest(BaseTest):
    def test_user(self):
        """Integration test for users."""

        # Create user
        self.assertIsNone(User.find_by_email(email=user_1["email"]))
        user = self.create_user(**user_1)
        self.assertIsNotNone(User.find_by_email(email=user_1["email"]))
        self.assertIsNotNone(User.find_by_id(1))

        # Test basic attributes
        self.assertEqual(user.id, 1)
        self.assertEqual(user.email, "test_user@gmail.com")
        self.assertTrue(user.check_password(user_1["password"]))
        self.assertEqual(repr(user), "<User test_user@gmail.com.>")

        # Delete user
        user.delete_from_db()
        self.assertIsNone(User.find_by_email(email=user_1["email"]))

    def test_portfolio(self):
        """Integration test for portfolios."""

        user = self.create_user(**user_1)

        # Create portfolio
        self.assertIsNone(Portfolio.query.filter_by(user=user).first())
        port = self.create_portfolio(**portfolio_1, user=user)
        self.assertIsNotNone(Portfolio.query.filter_by(user=user).all())
        self.assertIsNotNone(Portfolio.find_by_id(1))

        # Check basic attributes
        self.assertEqual(port.id, 1)
        self.assertEqual(port.name, "portfolio_1")
        self.assertEqual(port.reporting_currency, Currency.USD)
        self.assertEqual(port.portfolio_type, PortfolioType.margin)
        self.assertEqual(port.is_primary, False)
        self.assertEqual(port.user_id, 1)
        self.assertIsInstance(port.date, datetime)
        self.assertEqual(repr(port), "<Portfolio portfolio_1.>")

        # Delete portfolio
        port.delete_from_db()
        self.assertIsNone(Portfolio.query.filter_by(user=user).first())

    def test_position(self):
        """Integration test for positions."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)

        # Create position
        self.assertIsNone(Position.query.filter_by(portfolio=port).first())
        pos = self.create_position(**position_1, portfolio=port)
        self.assertIsNotNone(Position.query.filter_by(portfolio=port).all())
        self.assertIsNotNone(Position.find_by_id(1))

        # Check basic attributes
        self.assertEqual(pos.id, 1)
        self.assertEqual(pos.symbol, "AAPL")
        self.assertEqual(pos.name, "Apple Inc.")
        self.assertEqual(pos.security_type, SecurityType.Stock)
        self.assertEqual(pos.currency, Currency.USD)
        self.assertEqual(pos.portfolio_id, 1)
        self.assertEqual(repr(pos), "<Position AAPL.>")

        # Delete position
        pos.delete_from_db()
        self.assertIsNone(Position.query.filter_by(portfolio=port).first())

    def test_order(self):
        """Integration test for orders."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos = self.create_position(**position_1, portfolio=port)

        # Create order
        self.assertIsNone(Order.query.filter_by(position=pos).first())
        order = self.create_order(**order_1, position=pos)
        self.assertIsNotNone(Order.query.filter_by(position=pos).all())
        self.assertIsNotNone(Order.find_by_id(1))

        # Check basic attributes
        self.assertEqual(order.id, 1)
        self.assertEqual(order.symbol, "AAPL")
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.side, OrderSideType.Buy)
        self.assertEqual(order.avg_exec_price, 10.5)
        self.assertIsInstance(order.exec_time, datetime)
        self.assertEqual(order.fee, 0.123)
        self.assertEqual(repr(order), "<Order AAPL.>")

        # Delete order
        order.delete_from_db()
        self.assertIsNone(Order.query.filter_by(position=pos).first())

    def test_relationships(self):
        """Integration test for model relationships."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos = self.create_position(**position_1, portfolio=port)
        order = self.create_order(**order_1, position=pos)

        user.delete_from_db()
        self.assertIsNone(Portfolio.query.filter_by(user=user).first())
        self.assertIsNone(Position.query.filter_by(portfolio=port).first())
        self.assertIsNone(Order.query.filter_by(position=pos).first())

    @mock.patch(
        "src.market_data.yahoo.YFinance.get_current_quotes",
        return_value=pd.DataFrame([1], columns=["AAPL"]),
    )
    def test_portfolio_attributes(self, md=None):
        """Unit test for portfolio attributes."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)

        # Test primary attribute
        self.assertEqual(port.is_primary, False)
        port.set_as_primary()
        self.assertEqual(port.is_primary, True)

        # Test edit portfolio attribute
        port.edit("Hello World", Currency.USD, PortfolioType.rrsp, "^GSPC")
        self.assertEqual(port.name, "Hello World")
        self.assertEqual(port.reporting_currency, Currency.USD)
        self.assertEqual(port.portfolio_type, PortfolioType.rrsp)
        self.assertEqual(port.benchmark, "^GSPC")

        pos = self.create_position(**position_1, portfolio=port)
        self.create_order(**order_1, position=pos)
        self.create_order(**order_2, position=pos)
        self.assertEqual(port.total_mkt_value, 8)

    @mock.patch(
        "src.market_data.yahoo.YFinance.get_current_quotes",
        return_value=pd.DataFrame([1], columns=["AAPL"]),
    )
    def test_position_attributes(self, md=None):
        """Unit test for position attributes."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos = self.create_position(**position_1, portfolio=port)
        self.create_order(**order_1, position=pos)
        self.create_order(**order_2, position=pos)

        self.assertEqual(pos.open_quantity, 8)
        self.assertEqual(pos.market_cap, 8)
        self.assertEqual(pos.open, True)

    def test_order_attributes(self):
        """Unit test for position attributes."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos = self.create_position(**position_1, portfolio=port)
        order_buy = self.create_order(**order_1, position=pos)
        order_sell = self.create_order(**order_2, position=pos)

        self.assertEqual(order_buy.adjusted_quantity, 10)
        self.assertEqual(order_sell.adjusted_quantity, -2)

        # Edit Order
        order_buy.edit("FB", 20, OrderSideType.Sell, 100, datetime(2020, 1, 1), 10)
        self.assertEqual(order_buy.symbol, "FB")
        self.assertEqual(order_buy.quantity, 20)
        self.assertEqual(order_buy.side, OrderSideType.Sell)
        self.assertEqual(order_buy.avg_exec_price, 100)
        self.assertEqual(order_buy.exec_time, datetime(2020, 1, 1))
        self.assertEqual(order_buy.fee, 10)

    def test_to_df(self):

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos_1 = self.create_position(**position_1, portfolio=port)
        pos_2 = self.create_position(**position_2, portfolio=port)
        self.create_order(**order_1, position=pos_1)
        self.create_order(**order_2, position=pos_1)
        self.create_order(**order_3, position=pos_2)

        pos_1.orders_df()

        port.positions_df()

    @mock.patch(
        "src.market_data.yahoo.YFinance.get_current_quotes",
        return_value=pd.DataFrame([1], columns=["AAPL"]),
    )
    def test_to_dict(self, md=None):

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos = self.create_position(**position_1, portfolio=port)
        order_11 = self.create_order(**order_1, position=pos)
        order_12 = self.create_order(**order_2, position=pos)

        port_dict = {
            "id": 1,
            "Name": "portfolio_1",
            "Portfolio type": "Margin",
            "Reporting currency": "USD",
            "Primary": False,
            "Creation date": datetime(2020, 1, 1, 0, 0),
            "Total market value": "8.00",
            "Benchmark": "^GSPC",
            "Positions": [
                {
                    "ID": 1,
                    "Symbol": "AAPL",
                    "Name": "Apple Inc.",
                    "Security Type": "Common and preferred equities, ETFs, ETNs, units, ADRs, etc.",
                    "Currency": "USD",
                    "Market Cap": "8.00",
                    "Total Quantity": 8,
                    "Open": True,
                    "Orders": [
                        {
                            "ID": 2,
                            "symbol": "AAPL",
                            "quantity": 2,
                            "side": "Sell",
                            "avg_exec_price": 11.0,
                            "exec_time": "20-04-06 Mon 05:30",
                            "fee": 0.0,
                        },
                        {
                            "ID": 1,
                            "symbol": "AAPL",
                            "quantity": 10,
                            "side": "Buy",
                            "avg_exec_price": 10.5,
                            "exec_time": "20-01-03 Fri 01:01",
                            "fee": 0.123,
                        },
                    ],
                }
            ],
        }

        self.assertEqual(port.to_dict(), port_dict)

    def test_report(self):
        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos_1 = self.create_position(**position_1, portfolio=port)
        pos_2 = self.create_position(**position_2, portfolio=port)
        self.create_order(**order_1, position=pos_1)
        self.create_order(**order_2, position=pos_1)
        self.create_order(**order_3, position=pos_2)

        report = Report(portfolio=port)
        hey = report.get_returns()
