"""Periodic Alerts"""
# pylint: disable=no-member, invalid-name

from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import List, TYPE_CHECKING

from flask import Markup
from pandas import concat

from src.environment.base import Alert
from src.extensions import db
from src.market import Security
from src.market.alerts import MarketSignal
from src.analytics._return import periodic_return, weighted_periodic_return

if TYPE_CHECKING:
    from src.environment.portfolio import Portfolio
    from src.environment.user import User


class DailyReport(Alert):
    """Daily Alert."""

    __tablename__ = "daily_report"

    portfolio_id: int = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    portfolio: Portfolio = db.relationship("Portfolio", back_populates="daily_report")

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
        position_values = self.portfolio.position_values(start, end)
        benchmark_value = self.portfolio.benchmark.index(start, end).index

        periods = [1, 5, 22]
        columns = ["Daily Return", "Weekly Return", "Monthly Return"]

        sec_ret = list()
        port_ret = list()
        bench_ret = list()
        for period in periods:
            sec_ret.append(periodic_return(security_values, period).tail(1))
            bench_ret.append(periodic_return(benchmark_value, period).tail(1))
            port_ret.append(weighted_periodic_return(position_values, period).tail(1))

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

    security: Security = db.Column(db.PickleType(), nullable=False)
    alert_type: str
    signal: MarketSignal = db.Column(db.PickleType(), nullable=False)

    user_id: int = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user: User = db.relationship("User", back_populates="market_alerts")

    @property
    def subject(self) -> str:
        return f"Market alert for {self.security.symbol}"

    @property
    def email_template(self) -> str:
        return "email/market_alert.html"

    @property
    def recipients(self) -> List[str]:
        return [self.user.email]

    def condition(self) -> bool:
        current_value = self.security.value
        return self.signal.check(current_value.value)

    def generate_email_content(self) -> dict:
        date_time = datetime.now()
        return {
            "symbol": self.security.symbol,
            "alert_type": self.alert_type,
            "condition": "TBD",
            "target": self.signal,
            "current_value": self.security.value,
            "triggered_time": date_time.strftime("%d %B, %Y, %H:%M"),
        }


# class DailyNews(AlertBase):
#     pass

# class EconomicAlert(AlertBase):
#     pass
