from flask_login import current_user

from src.tests.base import BaseTest

from src.extensions import db
from src.environment.user_activities.user import User

from src.environment.user_activities.portfolio import Portfolio
from src.environment.user_activities.position import Position
from src.environment.user_activities.order import Order
from flask_login import login_user

email = "tuncutku@gmail.com"
password = "1234"


class TestPortfolioURLs(BaseTest):
    def login_test_user(self):
        test_user = User("test@gmail.com")
        test_user.set_password("test")
        test_user.save_to_db()
        self.client.post(
            "/users/login",
            data=dict(email="test@gmail.com", password="test"),
            follow_redirects=True,
        )

    def test_home_2(self):

        self.login_test_user()

        response = self.client.get("/portfolio/list")
        self.assertEqual(response.status_code, 200)
