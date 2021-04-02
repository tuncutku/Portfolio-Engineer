from flask import render_template, Markup
import pandas as pd

from datetime import datetime
from src.environment.utils.base import AlertBaseModel
from src.environment.utils.types import AlertPeriod
from src.extensions import db

from src.messanger.tasks.email import send_email


# class DailyReport(AlertBaseModel):
#     __tablename__ = "daily_reports"

#     portfolio_id = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
#     portfolio = db.relationship("Portfolio", back_populates="daily_report")

#     @property
#     def subject(self) -> str:
#         return f"Daily portfolio report {datetime.today().date().strftime('%d %B, %Y')}"

#     @property
#     def email_template(self):
#         return "email/daily_report.html"

#     def condition(self) -> bool:
#         return True

#     def _generate_email_content(self) -> dict:
#         report = self.portfolio.generate_report()

#         daily_return = report.get_returns().tail(1).T
#         weekly_return = report.get_returns(5).tail(1).T
#         monthly_return = report.get_returns(22).tail(1).T

#         df = pd.concat([daily_return, weekly_return, monthly_return], axis=1)
#         df.columns = ["Daily return", "Weekly return", "Monthly return"]

#         return {
#             "Main": {
#                 "Portfolio name": self.portfolio.name,
#                 "Portfolio type": self.portfolio.portfolio_type,
#                 "Creation date": self.portfolio.date.strftime("%d %B, %Y"),
#                 "Reporting currency": self.portfolio.reporting_currency,
#                 "Benchmark": self.portfolio.benchmark,
#             },
#             "Return_table": Markup(df.to_html()),
#         }

#     def send_async_email(self) -> None:
#         contents = self._generate_email_content()
#         send_email.apply_async(
#             subject=self.subject,
#             recipients=[self.portfolio.user.email],
#             html=render_template(self.email_template, **contents),
#         )


# class PriceAlert(AlertBaseModel):
#     period = AlertPeriod.TradingDaysEvery5Min
#     subject = ""

#     def condition(self):
#         return True

#     @property
#     def email_template(self):
#         pass


# class ReturnAlert(AlertBaseModel):
#     period = AlertPeriod.TradingDaysEvery5Min
#     subject = ""

#     def condition(self):
#         return True

#     @property
#     def email_template(self):
#         pass


# class NewsAlert(AlertBaseModel):
#     period = AlertPeriod.TradingDaysEvery5Min
#     subject = ""

#     def condition(self):
#         return True

#     @property
#     def email_template(self):
#         pass


# class EconomicAlert(AlertBaseModel):
#     period = AlertPeriod.TradingDaysEvery5Min
#     subject = ""

#     def condition(self):
#         return True

#     @property
#     def email_template(self):
#         pass
