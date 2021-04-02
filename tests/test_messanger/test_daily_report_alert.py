from datetime import date
import pandas as pd

from src.messanger.alerts.daily_report_alert import DailyReport


def test_portfolio_basics(client, db, user):
    """Integration test for portfolios."""

    report = DailyReport
