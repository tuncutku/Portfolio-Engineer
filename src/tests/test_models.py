from sqlalchemy.exc import StatementError
from datetime import datetime

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

        self.assertIsNone(User.find_by_email(email=user_1["email"]))
        user = self.create_user(**user_1)
        self.assertIsNotNone(User.find_by_email(email=user_1["email"]))
        self.assertTrue(user.check_password(user_1["password"]))
        user.delete_from_db()
        self.assertIsNone(User.find_by_email(email=user_1["email"]))

    def test_portfolio(self):
        """Integration test for portfolios."""

        user = self.create_user(**user_1)

        self.assertIsNone(Portfolio.query.filter_by(user=user).first())
        port = self.create_portfolio(**portfolio_1, user=user)
        self.assertIsNotNone(Portfolio.query.filter_by(user=user).all())

        port_id = port.id
        self.assertIsNotNone(Portfolio.find_by_id(port_id))

        port.delete_from_db()
        self.assertIsNone(Portfolio.query.filter_by(user=user).first())

    def test_position(self):
        """Integration test for positions."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)

        self.assertIsNone(Position.query.filter_by(portfolio=port).first())
        pos = self.create_position(**position_1, portfolio=port)
        self.assertIsNotNone(Position.query.filter_by(portfolio=port).all())
        pos.delete_from_db()
        self.assertIsNone(Position.query.filter_by(portfolio=port).first())

    def test_order(self):
        """Integration test for orders."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos = self.create_position(**position_1, portfolio=port)

        self.assertIsNone(Order.query.filter_by(position=pos).first())
        order = self.create_order(**order_1, position=pos)
        self.assertIsNotNone(Order.query.filter_by(position=pos).all())
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

    def test_position_attributes(self):
        """Unit test for position attributes."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos = self.create_position(**position_1, portfolio=port)
        self.create_order(**order_1, position=pos)
        self.create_order(**order_2, position=pos)

        self.assertEqual(pos.open_quantity, 8)
        self.assertEqual(pos.market_cap, 1082.96)
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
