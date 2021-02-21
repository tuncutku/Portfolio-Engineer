from flask_login import current_user

from src.tests.utils.base import BaseTest
from src.environment.user import User
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order

from src.environment.utils.types import *


class TestPortfolioURLs(BaseTest):
    def test_portfolio_list(self):

        self.login_user()

        response = self.client.get("/portfolio/list")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")
        self.assertContext("port_list", [self.portfolio_test.to_dict()])

    def test_add_portfolio(self):

        self.login_user()

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

    def test_add_portfolio_form(self):
        pass

    def test_edit_portfolio(self):
        self.login_user()

        response = self.client.get("portfolio/edit/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/edit_portfolio.html")
        self.assertTrue("Edit portfolio" in response.get_data(as_text=True))
        self.assertTrue("portfolio_1" in response.get_data(as_text=True))
        self.assertTrue("Margin" in response.get_data(as_text=True))
        self.assertTrue("USD" in response.get_data(as_text=True))

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
        self.assertEqual(self.portfolio_test.name, "edited_portfolio")
        self.assertEqual(self.portfolio_test.portfolio_type, PortfolioType.custom)
        self.assertEqual(self.portfolio_test.reporting_currency, Currency.CAD)

    def test_delete_portfolio(self):
        self.login_user()

        response = self.client.get(
            "portfolio/delete/1",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")
        self.assertIsNone(Portfolio.query.filter_by(user=self.user_test).first())

    def test_set_portfolio_primary(self):
        self.login_user()

        portfolio = Portfolio.find_by_id(1)
        self.assertEqual(portfolio.is_primary, False)
        response = self.client.get(
            "portfolio/set_primary/1",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("portfolio/list_portfolios.html")
        portfolio = Portfolio.find_by_id(1)
        self.assertEqual(portfolio.is_primary, True)
