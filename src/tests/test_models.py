from src.tests.base import BaseTest

from src.extensions import db
from src.environment.user_activities.user import User
from src.environment.user_activities.portfolio import Portfolio
from src.environment.user_activities.position import Position
from src.environment.user_activities.order import Order

email = "tuncutku@gmail.com"
password = "1234"


class ModelTest(BaseTest):
    def test_user(self):

        self.assertIsNone(User.find_by_email(email=email))

        user = User(email=email)
        user.set_password(password)
        user.save_to_db()

        self.assertIsNotNone(User.find_by_email(email=email))
        self.assertTrue(user.check_password(password))

        user.delete_from_db()

        self.assertIsNone(User.find_by_email(email=email))

    def test_portfolio(self):

        user = User(email=email)
        user.set_password(password)
        user.save_to_db()

        self.assertIsNone(Portfolio.query.filter_by(user=user).first())

        portfolio_1 = Portfolio(
            name="portfolio_1",
            portfolio_type="invalid",
            reporting_currency="CAD",
            user=user,
        )

        portfolio_2 = Portfolio(
            name="portfolio_2",
            portfolio_type="TFSA",
            reporting_currency="USD",
            user=user,
        )

        portfolio_1.save_to_db()
        portfolio_2.save_to_db()

        self.assertIsNotNone(Portfolio.query.filter_by(user=user).all())
        portfolio_1.delete_from_db()
        self.assertIsNone(Portfolio.query.filter_by(name="portfolio_1").first())
        user.delete_from_db()
        self.assertIsNone(Portfolio.query.filter_by(name="portfolio_2").first())
