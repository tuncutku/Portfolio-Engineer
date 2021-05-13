"""Alert"""

# pylint: disable=no-member, invalid-name
from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import List, TYPE_CHECKING

from flask import Markup
from pandas import concat

from src.environment.base import Alert
from src.extensions import db
from src.analytics._return import single_periodic_return, weighted_periodic_return

if TYPE_CHECKING:
    from src.environment.portfolio import Portfolio


class DailyReport(Alert):
    """Daily Alert."""

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

        # Workaround in case end date data is not valid.
        for value in [security_values, position_values, benchmark_value]:
            value.ffill(inplace=True)

        periods = [1, 5, 22]
        columns = ["Daily Return", "Weekly Return", "Monthly Return"]

        sec_ret = list()
        port_ret = list()
        bench_ret = list()
        for period in periods:
            sec_ret.append(single_periodic_return(security_values, period).tail(1))
            bench_ret.append(single_periodic_return(benchmark_value, period).tail(1))
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
                "Current value": self.portfolio.current_value,
            },
            "Return_table": Markup(df.to_html()),
        }


# class PriceAlert(AlertBase):
#     pass


# class ReturnAlert(AlertBase):
#     pass


# class NewsAlert(AlertBase):
#     pass


# class EconomicAlert(AlertBase):
#     pass
