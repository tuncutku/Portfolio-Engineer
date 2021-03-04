from flask_testing import TestCase
from datetime import datetime
from src.extensions import db
from src import create_app

from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from src.tests.utils.sample_data import *


class BaseTest(TestCase):

    test_user = None
    test_portfolio = None
    test_position = None
    test_order = None

    def create_app(self):
        return create_app("config.TestConfig")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_user(self, email: str, password: str) -> User:

        user = User(email=email)
        user.set_password(password)
        user.save_to_db()
        return user

    def create_portfolio(
        self,
        name: str,
        portfolio_type: str,
        reporting_currency: str,
        date: datetime,
        benchmark: str,
        user: User,
    ) -> Portfolio:

        portfolio = Portfolio(
            name=name,
            portfolio_type=portfolio_type,
            reporting_currency=reporting_currency,
            date=datetime(2020, 1, 1),
            benchmark=benchmark,
            user=user,
        )
        portfolio.save_to_db()
        return portfolio

    def create_position(
        self,
        symbol: str,
        name: str,
        security_type: str,
        currency: str,
        portfolio: Portfolio,
    ) -> Position:

        position = Position(
            symbol=symbol,
            name=name,
            security_type=security_type,
            currency=currency,
            portfolio=portfolio,
        )
        position.save_to_db()
        return position

    def create_order(
        self,
        symbol: str,
        quantity: int,
        side: str,
        avg_exec_price: float,
        exec_time: datetime,
        fee: float,
        position: Position,
    ) -> Order:

        order = Order(
            symbol=symbol,
            quantity=quantity,
            side=side,
            avg_exec_price=avg_exec_price,
            exec_time=exec_time,
            fee=fee,
            position=position,
        )
        order.save_to_db()
        return order

    def login_user(self):
        """Log in test user for URL tests."""
        self.user_test = self.create_user(**user_1)
        self.portfolio_test = self.create_portfolio(**portfolio_1, user=self.user_test)
        self.position_test = self.create_position(
            **position_1, portfolio=self.portfolio_test
        )
        self.order_test = self.create_order(**order_1, position=self.position_test)

        self.client.post("/users/login", data=dict(**user_1))
