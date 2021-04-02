import pandas as pd

from tests.sample_data import *
from tests.utils import create_user, create_portfolio, create_position, create_order

from src.environment.position import Position


def test_position_basics(client, db):
    """Integration test for positions."""

    user = create_user(**user_1)
    port = create_portfolio(**portfolio_1, user=user)

    # Create position
    assert Position.query.filter_by(portfolio=port).first() == None
    pos = create_position(**position_1, portfolio=port)
    assert Position.query.filter_by(portfolio=port).all() != None
    assert Position.find_by_id(1) != None

    # Check basic attributes
    assert pos.id == 1
    assert pos.symbol == "AAPL"
    assert pos.name == "Apple Inc."
    assert pos.security_type == SecurityType.Equity
    assert pos.currency == Currency.USD
    assert pos.portfolio_id == 1
    assert repr(pos) == "<Position AAPL.>"

    # Delete position
    pos.delete_from_db()
    assert Position.query.filter_by(portfolio=port).first() == None


def test_position_attributes(client, db, mocker):
    """Unit test for position attributes."""

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

    assert pos.open_quantity == 8
    assert pos.market_cap == 8
    assert pos.open == True
