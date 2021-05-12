"""Alert"""

# pylint: disable=no-member, invalid-name
from __future__ import annotations

from datetime import datetime, date, timedelta
from typing import TYPE_CHECKING

from flask import Markup
import pandas as pd

from src.environment.base import Alert
from src.extensions import db
from src.analytics._return import single_periodic_return

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
    def email_template(self):
        return "email/daily_report.html"

    @property
    def recipients(self):
        return self.portfolio.user.email

    def condition(self) -> bool:
        return True

    def generate_email_content(self) -> dict:

        end = date.today()
        start = end - timedelta(32)

        historical_index = self.portfolio.historical_value(start, end)

        periods = [1, 5, 22]
        columns = ["Daily return", "Weekly return", "Monthly return"]
        returns = [
            single_periodic_return(historical_index.index, period).tail(1).T
            for period in periods
        ]
        df = pd.concat(returns, axis=1)
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
