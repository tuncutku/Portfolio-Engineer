from sqlalchemy.exc import StatementError
from datetime import datetime
from unittest import mock
import pandas as pd

from tests.utils.base import BaseTest
from tests.utils.sample_data import *

from src.extensions import db
from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from src.reports.report import Report


class ModelTest(BaseTest):
    def test_report(self):
        user = self.create_user(**user_1)
        port = self.create_portfolio(**portfolio_1, user=user)
        pos_1 = self.create_position(**position_1, portfolio=port)
        pos_2 = self.create_position(**position_2, portfolio=port)
        self.create_order(**order_1, position=pos_1)
        self.create_order(**order_2, position=pos_1)
        self.create_order(**order_3, position=pos_2)

        report = Report(portfolio=port)
        hey = report.get_returns()
