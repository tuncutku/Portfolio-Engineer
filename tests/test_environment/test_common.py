from datetime import date
import pandas as pd

from tests.sample_data import *
from tests.utils import create_user, create_portfolio, create_position, create_order

from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order

# from src.environment.alerts import DailyReport


def test_relationships(client, _db, test_data):
    """Integration test for model relationships."""

    test_data.user.delete_from_db()
    assert Portfolio.query.filter_by(user=test_data.user).first() is None
    assert Position.query.filter_by(portfolio=test_data.portfolio).first() is None
    assert Order.query.filter_by(position=test_data.position).first() is None
