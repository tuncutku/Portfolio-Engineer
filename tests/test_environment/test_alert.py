from datetime import date
import pandas as pd

from tests.sample_data import *
from tests.utils import create_user, create_portfolio, create_position, create_order

from src.environment.portfolio import Portfolio
from src.environment.order import Order


def test_alert_basics(client, db):
    """Integration test for alerts."""

    user = create_user(**user_1)
    port = create_portfolio(**portfolio_1, user=user)
    pos = create_position(**position_1, portfolio=port)
    order_11 = create_order(**order_1, position=pos)
    order_12 = create_order(**order_2, position=pos)

    # daily_report = DailyReport(portfolio=port)
    # daily_report.generate_email()