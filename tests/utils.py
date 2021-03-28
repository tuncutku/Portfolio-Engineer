from datetime import datetime

from src.extensions import db
from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from src.environment.alert import DailyReport
from src.reports.report import Report

from tests.sample_data import *


def create_user(email: str, password: str) -> User:

    user = User(email=email)
    user.set_password(password)
    user.save_to_db()
    return user


def create_portfolio(
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
        date=date,
        benchmark=benchmark,
        user=user,
    )
    portfolio.save_to_db()
    return portfolio


def create_position(
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
