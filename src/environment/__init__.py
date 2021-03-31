from src.environment.alert import DailyReport
from src.environment.portfolio import Portfolio

from flask_sqlalchemy import event


@event.listens_for(Portfolio, "after_insert")
def add_daily_alert(mapper, connection, target):
    report = DailyReport(portfolio=target)
