from tests.utils.base import BaseTest
from tests.utils.sample_data import *

from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from src.environment.alert import DailyReport
from src.reports.report import Report

from src.messenger.tasks import send_email, daily_report_task


class MessangerTest(BaseTest):
    def test_periodic_task(self):
        """Test messenger tasks."""

        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos = self.create_position(**position_1, portfolio=port)
        order_11 = self.create_order(**order_1, position=pos)
        order_12 = self.create_order(**order_2, position=pos)

        daily_report_object = DailyReport(portfolio=port)
        daily_report_object.activate()

        daily_report_task()
