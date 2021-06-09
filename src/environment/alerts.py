"""Periodic Alerts"""
# pylint: disable=no-member, invalid-name

from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import List, TYPE_CHECKING

from flask import Markup
from pandas import concat

from src.environment.base import Alert
from src.extensions import db
from src.market.signal import Signal
from src.analytics._return import periodic_return, weighted_periodic_return

if TYPE_CHECKING:
    from src.environment.portfolio import Portfolio
    from src.environment.user import User


class DailyReport(Alert):
    """Daily Alert."""

    __tablename__ = "daily_report"

    portfolio_id: int = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    portfolio: Portfolio = db.relationship("Portfolio", back_populates="daily_report")

    def __init__(self, portfolio: Portfolio) -> None:
        self.portfolio = portfolio

    @property
    def subject(self) -> str:
        return f"Daily portfolio report {datetime.today().date().strftime('%d %B, %Y')}"

    @property
    def email_template(self) -> str:
        return "email/daily_report.html"

    @property
    def recipients(self) -> List[str]:
        return [self.portfolio.user.email]

    def condition(self) -> bool:
        return True

    def generate_email_content(self) -> dict:

        end = date.today()
        start = end - timedelta(40)

        security_values = self.portfolio.security_values(start, end)
        benchmark_value = self.portfolio.benchmark.index(start, end).index
        position_quantities = self.portfolio.position_quantities(start, end)

        periods = [1, 5, 22]
        columns = ["Daily Return", "Weekly Return", "Monthly Return"]

        sec_ret = [
            periodic_return(security_values, period).tail(1) for period in periods
        ]
        bench_ret = [
            periodic_return(benchmark_value, period).tail(1) for period in periods
        ]
        port_ret = [
            weighted_periodic_return(security_values, position_quantities, period).tail(
                1
            )
            for period in periods
        ]

        df = concat([concat(port_ret), concat(bench_ret), concat(sec_ret)], axis=1).T
        df.columns = columns

        return {
            "Main": {
                "Portfolio name": self.portfolio.name,
                "Portfolio type": self.portfolio.portfolio_type,
                "Creation date": self.portfolio.date.strftime("%d %B, %Y"),
                "Benchmark": self.portfolio.benchmark,
                "Reporting currency": self.portfolio.reporting_currency,
                "Current market value": round(self.portfolio.current_value(), 2),
            },
            "Return_table": Markup(df.to_html()),
        }


class MarketAlert(Alert):
    """Price Alert."""

    __tablename__ = "market_alert"

    signal: Signal = db.Column(db.PickleType(), nullable=False)

    user_id: int = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user: User = db.relationship("User", back_populates="market_alerts")

    def __init__(self, signal: Signal) -> None:
        self.signal = signal
        self.active = True

    @property
    def subject(self) -> str:
        return f"Market alert for {self.signal.security.symbol}"

    @property
    def email_template(self) -> str:
        return "email/market_alert.html"

    @property
    def recipients(self) -> List[str]:
        return [self.user.email]

    def condition(self) -> bool:
        return self.signal.apply_operator()

    def generate_email_content(self) -> dict:
        date_time = datetime.now()
        return {
            "symbol": self.signal.security.symbol,
            "signal": self.signal,
            "current_value": self.signal.value,
            "triggered_time": date_time.strftime("%d %B, %Y, %H:%M"),
        }


# class DailyNews(AlertBase):
#     pass

# class EconomicAlert(AlertBase):
#     pass
