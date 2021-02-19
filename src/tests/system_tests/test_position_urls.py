from flask_login import current_user

from src.tests.utils.base import BaseTest
from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order
from src.environment.types import PortfolioType, Currency


class TestPositionURLs(BaseTest):
    def test_position_details(self):

        self.login_user()

        response = self.client.get("position/1/details")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("position/position_details.html")
        self.assertContext("position", self.position_test.to_dict())

    def test_close_position(self):

        self.login_user()

        self.assertEqual(self.position_test.open, True)
        response = self.client.get(
            "position/1/close",
            follow_redirects=True,
        )
        self.assertEqual(self.position_test.open, False)