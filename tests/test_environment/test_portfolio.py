from datetime import date
import pandas as pd

from tests.sample_data import portfolio_2
from src.environment.portfolio import Portfolio, PortfolioType
from src.market import Currency


def test_portfolio_basics(client, _db, test_data):
    """Integration test for portfolios."""

    # Create portfolio
    assert Portfolio.find_by_id(2) is None
    port = Portfolio(**portfolio_2, user=test_data.user)
    assert Portfolio.find_by_id(2) is not None

    # Check basic attributes
    assert port.id == 2
    assert port.name == "portfolio_2"
    assert port.reporting_currency == Currency("CAD")
    assert port.portfolio_type == PortfolioType.cash
    assert port.primary is False
    assert port.user_id == 1
    assert isinstance(port.date, date)
    assert repr(port) == "<Portfolio portfolio_2.>"

    # Delete portfolio
    port.delete_from_db()
    assert Portfolio.find_by_id(2) is None


def test_portfolio_attributes(client, _db, mocker, test_data):
    """Unit test for portfolio attributes."""

    def mock_func(self, decimal=2):
        return pd.DataFrame([1], columns=["AAPL"])

    mocker.patch(
        "src.market.provider.YFinance.get_current_quotes",
        mock_func,
    )

    port = test_data.portfolio

    # Test primary attribute
    assert port.primary is False
    port.set_as_primary()
    assert port.primary is True

    # Test edit portfolio attribute
    port.edit("Hello World", Currency("CAD"), PortfolioType.rrsp, "^GSPC")
    assert port.name == "Hello World"
    assert port.reporting_currency == Currency("CAD")
    assert port.portfolio_type == PortfolioType.rrsp
    assert port.benchmark == "^GSPC"
