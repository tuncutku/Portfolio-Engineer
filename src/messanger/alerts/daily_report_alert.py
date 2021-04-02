from flask import render_template, Markup
import pandas as pd

from datetime import datetime
from dataclasses import dataclass

from src.messanger.alerts.base import AlertBase

from src.reports.report import Report


@dataclass
class DailyReport(AlertBase):

    # report: Report

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
