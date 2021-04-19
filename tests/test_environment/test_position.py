from pandas import DataFrame
from datetime import date

from tests.sample_data import *
from src.environment.position import Position
from src.environment.order import Order
from src.market import Equity


def test_position_basics(client, _db, test_data):
    """Integration test for positions."""

    # Create position
    assert Position.find_by_id(2) is None
    pos = Position(**position_2, portfolio=test_data.portfolio)
    assert Position.find_by_id(2) is not None

    # Check basic attributes
    assert pos.id == 2
    assert pos.security == Equity(asset_currency="USD", symbol="FB")
    assert repr(pos) == "<Position asset_currency=USD symbol=FB.>"

    # Delete position
    pos.delete_from_db()
    assert Position.find_by_id(2) is None


def test_position_attributes(client, _db, mocker, test_data):
    """Unit test for position attributes."""

    def mock_func(self, decimal=2):
        return DataFrame([1], columns=["AAPL"])

    mocker.patch(
        "src.market.provider.YFinance.get_current_quotes",
        mock_func,
    )

    assert Order.find_by_id(2) is None
    pos = test_data.position
    pos.add_order(**order_1_2)
    assert Order.find_by_id(2) is not None

    pos.open_quantity == 8

    df = DataFrame(
        data=[[0.123, 10, 10.5], [0.000, -2, 11.0]],
        index=[date(2020, 1, 3), date(2020, 4, 6)],
        columns=["Fee", "Quantity", "Quote"],
    )
    assert df.equals(pos.orders_df)

    # assert pos.open_quantity == 8
    # assert pos.market_cap == 8
    # assert pos.open is True
