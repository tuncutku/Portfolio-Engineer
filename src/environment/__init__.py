from src.environment.alerts import DailyReport
from src.environment.portfolio import Portfolio
from src.environment.position import Position

from flask_sqlalchemy import event


@event.listens_for(Portfolio, "after_insert")
def add_daily_alert(mapper, connection, target):
    report = DailyReport(portfolio=target)


@event.listens_for(Position, "before_insert")
def add_new_position(mapper, connection, target):
    pass
    # report = DailyReport(portfolio=target)
