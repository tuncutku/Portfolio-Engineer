from flask_login import current_user

from src.tests.utils.sample_data import *
from src.tests.utils.base import BaseTest
from src.environment.user_activities.user import User
from src.environment.user_activities.portfolio import Portfolio, PortfolioType, Currency
from src.environment.user_activities.position import Position
from src.environment.user_activities.order import Order


email = "tuncutku@gmail.com"
password = "1234"


class TestPortfolioURLs(BaseTest):
    def login_user(self):
        """Log in test user for URL tests."""
        user = self.create_user(**user_1)
        portfolio = self.create_portfolio(**portfolio_1, user=user)
        position = self.create_position(**position_1, portfolio=portfolio)
        order = self.create_order(**order_1, position=position)

        self.client.post("/users/login", data=dict(**user_1))

        return portfolio

    def test_portfolio_list(self):

        portfolio = self.login_user()

        response = self.client.get("/portfolio/list")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")
        self.assertContext("port_list", [portfolio.to_dict()])

    def test_add_portfolio(self):

        portfolio = self.login_user()
        response = self.client.get("portfolio/add_portfolio")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Add new custom portfolio" in response.get_data(as_text=True))

        response = self.client.post(
            "portfolio/add_portfolio",
            data=dict(
                port_name="New",
                port_type=PortfolioType.margin,
                port_reporting_currency=Currency.USD,
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")

        new_portfolio = Portfolio.find_by_id(2)

        self.assertEqual(new_portfolio.name, "New")
        self.assertEqual(new_portfolio.portfolio_type, PortfolioType.margin)
        self.assertEqual(new_portfolio.reporting_currency, Currency.USD)

    def test_edit_portfolio(self):
        portfolio = self.login_user()

        response = self.client.get("portfolio/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Edit portfolio" in response.get_data(as_text=True))

        response = self.client.post(
            "portfolio/edit/1",
            data=dict(
                port_name="edited_portfolio",
                port_type=PortfolioType.custom,
                port_reporting_currency=Currency.CAD,
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")

        self.assertEqual(portfolio.name, "edited_portfolio")
        self.assertEqual(portfolio.portfolio_type, PortfolioType.custom)
        self.assertEqual(portfolio.reporting_currency, Currency.CAD)
