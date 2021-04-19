from datetime import date
import pandas as pd

from tests.sample_data import *

from src.environment.portfolio import Portfolio
from src.environment.order import Order


def test_alert_basics(client, _db, test_data):
    """Integration test for alerts."""

    a = 1
