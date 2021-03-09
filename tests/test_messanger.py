from tests.utils.base import BaseTest
from tests.utils.sample_data import *

from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from src.reports.report import Report

from src.messenger.tasks import periodic_report, send_async_email


class MessangerTest(BaseTest):
    def test_periodic_task(self):
        """Test messenger tasks."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
