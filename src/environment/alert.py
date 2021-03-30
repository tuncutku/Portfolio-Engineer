from flask import render_template, Markup
import pandas as pd

from datetime import datetime
from src.environment.utils.base import AlertBaseModel
from src.environment.utils.types import AlertPeriod
from src.extensions import db


class DailyReport(AlertBaseModel):
    period = AlertPeriod.TradingDaysDaily
    subject = f"Daily portfolio report {datetime.today().date().strftime('%d %B, %Y')}"
    template = "email/daily_report.html"

    portfolio_id = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    portfolio = db.relationship("Portfolio", back_populates="daily_report")

    def condition(self) -> bool:
        return True

    def _generate_contents(self) -> dict:
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

    def generate_email(self):
        contents = self._generate_contents()
        return {
            "subject": self.subject,
            "recipient": [self.portfolio.user.email],
            "html": render_template(self.template, **contents),
        }


class TechnicalAlert(AlertBaseModel):
    period = AlertPeriod.TradingDaysEvery5Min
    subject = ""

    def condition(self):
        return True

    @property
    def email_template(self):
        pass


class NewsAlert(AlertBaseModel):
    period = AlertPeriod.TradingDaysEvery5Min
    subject = ""

    def condition(self):
        return True

    @property
    def email_template(self):
        pass


class EconomicAlert(AlertBaseModel):
    period = AlertPeriod.TradingDaysEvery5Min
    subject = ""

    def condition(self):
        return True

    @property
    def email_template(self):
        pass
