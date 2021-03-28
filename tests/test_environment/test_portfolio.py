from datetime import date
import pandas as pd

from tests.sample_data import *
from tests.utils import create_user, create_portfolio, create_position, create_order

from src.environment.portfolio import Portfolio


def test_portfolio_basics(client, db):
    """Integration test for portfolios."""

    user = create_user(**user_1)

    # Create portfolio
    assert Portfolio.query.filter_by(user=user).first() == None
    port = create_portfolio(**portfolio_1, user=user)
    assert Portfolio.query.filter_by(user=user).all() != None
    assert Portfolio.find_by_id(1) != None

    # Check basic attributes
    assert port.id == 1
    assert port.name == "portfolio_1"
    assert port.reporting_currency == Currency.USD
    assert port.portfolio_type == PortfolioType.margin
    assert port.is_primary == False
    assert port.user_id == 1
    assert isinstance(port.date, date)
    assert repr(port) == "<Portfolio portfolio_1.>"

    # Delete portfolio
    port.delete_from_db()
    assert Portfolio.query.filter_by(user=user).first() == None


def test_portfolio_attributes(client, db, mocker):
    """Unit test for portfolio attributes."""

    def mock_func(self, decimal=2):
        return pd.DataFrame([1], columns=["AAPL"])

    mocker.patch(
        "src.market_data.yahoo.YFinance.get_current_quotes",
        mock_func,
    )

    user = create_user(**user_1)
    port = create_portfolio(**portfolio_1, user=user)
    pos = create_position(**position_1, portfolio=port)
    create_order(**order_1, position=pos)
    create_order(**order_2, position=pos)

    # Test primary attribute
    assert port.is_primary == False
    port.set_as_primary()
    assert port.is_primary == True

    # Test edit portfolio attribute
    port.edit("Hello World", Currency.USD, PortfolioType.rrsp, "^GSPC")
    assert port.name == "Hello World"
    assert port.reporting_currency == Currency.USD
    assert port.portfolio_type == PortfolioType.rrsp
    assert port.benchmark == "^GSPC"
    assert port.total_mkt_value == 8
