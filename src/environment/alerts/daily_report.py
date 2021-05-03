from __future__ import annotations

from flask import render_template, Markup
import pandas as pd
from typing import TYPE_CHECKING

from datetime import datetime
from src.environment.utils.base import AlertBase
from src.extensions import db

if TYPE_CHECKING:
    from src.environment.portfolio import Portfolio


class DailyReport(AlertBase):

    portfolio_id: int = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    portfolio: Portfolio = db.relationship("Portfolio", back_populates="daily_report")

    @property
    def subject(self) -> str:
        return f"Daily portfolio report {datetime.today().date().strftime('%d %B, %Y')}"

    @property
    def email_template(self):
        return "email/daily_report.html"

    def condition(self) -> bool:
        return True

    def generate_email_content(self) -> dict:
        report = self.portfolio.generate_report()

        daily_return = report.get_returns().tail(1).T
        weekly_return = report.get_returns(5).tail(1).T
        monthly_return = report.get_returns(22).tail(1).T

        df = pd.concat([daily_return, weekly_return, monthly_return], axis=1)
        df.columns = ["Daily return", "Weekly return", "Monthly return"]

        return {
            "Main": {
                "Portfolio name": self.portfolio.name,
                "Portfolio type": self.portfolio.portfolio_type,
                "Creation date": self.portfolio.date.strftime("%d %B, %Y"),
                "Reporting currency": self.portfolio.reporting_currency,
                "Benchmark": self.portfolio.benchmark,
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
