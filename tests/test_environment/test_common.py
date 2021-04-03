from datetime import date
import pandas as pd

from tests.sample_data import *
from tests.utils import create_user, create_portfolio, create_position, create_order

from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order

# from src.environment.alerts import DailyReport


port_dict = {
    "id": 1,
    "Name": "portfolio_1",
    "Portfolio type": "Margin",
    "Reporting currency": "USD",
    "Primary": False,
    "Creation date": date(2020, 1, 1),
    "Total market value": "8.00",
    "Benchmark": "^GSPC",
    "Positions": [
        {
            "ID": 1,
            "Symbol": "AAPL",
            "Name": "Apple Inc.",
            "Security Type": "Common and preferred equities",
            "Currency": "USD",
            "Market Cap": "8.00",
            "Total Quantity": 8,
            "Open": True,
            "Orders": [
                {
                    "ID": 2,
                    "symbol": "AAPL",
                    "quantity": 2,
                    "side": "Sell",
                    "exec_price": 11.0,
                    "exec_time": "20-04-06 Mon 00:00",
                    "fee": 0.0,
                },
                {
                    "ID": 1,
                    "symbol": "AAPL",
                    "quantity": 10,
                    "side": "Buy",
                    "exec_price": 10.5,
                    "exec_time": "20-01-03 Fri 00:00",
                    "fee": 0.123,
                },
            ],
        }
    ],
}


def test_relationships(client, db):
    """Integration test for model relationships."""

    user = create_user(**user_1)
    port = create_portfolio(**portfolio_1, user=user)
    pos = create_position(**position_1, portfolio=port)
    order = create_order(**order_1, position=pos)

    user.delete_from_db()
    assert Portfolio.query.filter_by(user=user).first() == None
    assert Position.query.filter_by(portfolio=port).first() == None
    assert Order.query.filter_by(position=pos).first() == None


def test_to_df(client, db):
    """Integration test for model dataframe."""

    user = create_user(**user_1)
    port = create_portfolio(**portfolio_1, user=user)
    pos_1 = create_position(**position_1, portfolio=port)
    pos_2 = create_position(**position_2, portfolio=port)
    create_order(**order_1, position=pos_1)
    create_order(**order_2, position=pos_1)
    create_order(**order_3, position=pos_2)

    pos_1.orders_df()
    port.positions_df()


def test_to_dict(client, db, mocker):
    """Integration test for dict."""

    def mock_func(self, decimal=2):
        return pd.DataFrame([1], columns=["AAPL"])

    mocker.patch(
        "src.market_data.provider.YFinance.get_current_quotes",
        mock_func,
    )

    user = create_user(**user_1)
    port = create_portfolio(**portfolio_1, user=user)
    pos = create_position(**position_1, portfolio=port)
    order_11 = create_order(**order_1, position=pos)
    order_12 = create_order(**order_2, position=pos)

    assert port.to_dict() == port_dict
