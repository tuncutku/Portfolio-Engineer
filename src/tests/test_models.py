from sqlalchemy.exc import StatementError
from datetime import datetime
from unittest import mock

from src.tests.utils.base import BaseTest
from src.tests.utils.sample_data import *

from src.extensions import db
from src.environment.user_activities.user import User
from src.environment.user_activities.portfolio import Portfolio
from src.environment.user_activities.position import Position
from src.environment.user_activities.order import Order


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

    @mock.patch("src.market_data.yahoo.YFinance.get_quote", return_value=1)
    def test_portfolio_attributes(self, md):
        """Unit test for portfolio attributes."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)

        # Test primary attribute
        self.assertEqual(port.is_primary, False)
        port.set_as_primary()
        self.assertEqual(port.is_primary, True)

        # Test edit portfolio attribute
        port.edit("Hello World", Currency.USD, PortfolioType.rrsp)
        self.assertEqual(port.name, "Hello World")
        self.assertEqual(port.reporting_currency, Currency.USD)
        self.assertEqual(port.portfolio_type, PortfolioType.rrsp)

        pos = self.create_position(**position_1, portfolio=port)
        self.create_order(**order_1, position=pos)
        self.create_order(**order_2, position=pos)
        self.assertEqual(port.total_mkt_value, 8)

    @mock.patch("src.market_data.yahoo.YFinance.get_quote", return_value=1)
    def test_position_attributes(self, md):
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
