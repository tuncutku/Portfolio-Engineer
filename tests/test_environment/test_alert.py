from datetime import date
import pandas as pd

from tests.sample_data import *

from src.environment.portfolio import Portfolio
from src.environment.order import Order


def test_alert_basics(client, db, user):
    """Integration test for alerts."""

    port = Portfolio.find_by_id(1)
    port.daily_report
    # daily_report.generate_email()