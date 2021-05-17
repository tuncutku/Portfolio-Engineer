"""Environment objects"""

# pylint: disable=# pylint: disable=no-member, unused-argument

from flask_sqlalchemy import event

from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from src.environment.alerts import DailyReport, PriceAlert, Alert
from src.extensions import db


@event.listens_for(Portfolio, "after_insert")
def add_daily_alert(mapper, connection, target):
    """Add a daily report when a portfolio object is formed."""

    @event.listens_for(db.session, "after_flush", once=True)
    def receive_after_flush(session, context):
        new_daily_report = DailyReport(portfolio=target)
        db.session.add(new_daily_report)
