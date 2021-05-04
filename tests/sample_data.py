"""Sample data for tests"""

from datetime import datetime, date
from pandas import Series
import pytz

from src.environment.utils.types import PortfolioType
from src.environment.order import OrderSideType

from src.market import (
    Currency,
    Equity,
    Index,
    IndexValue,
    SingleValue,
)

######## Environment data ########

order_1 = {
    "quantity": 10,
    "direction": OrderSideType.Buy,
    "cost": 130,
    "time": datetime(2020, 2, 3, tzinfo=pytz.utc),
}
order_2 = {
    "quantity": 2,
    "direction": OrderSideType.Sell,
    "cost": 122,
    "time": datetime(2020, 7, 1, tzinfo=pytz.utc),
}
order_3 = {
    "quantity": 14,
    "direction": OrderSideType.Sell,
    "cost": 126,
    "time": datetime(2021, 1, 13, tzinfo=pytz.utc),
}
order_4 = {
    "quantity": 20,
    "direction": OrderSideType.Buy,
    "cost": 100,
    "time": datetime(2019, 11, 13, tzinfo=pytz.utc),
}
order_5 = {
    "quantity": 10,
    "direction": OrderSideType.Buy,
    "cost": 111,
    "time": datetime(2020, 7, 1, tzinfo=pytz.utc),
}
order_6 = {
    "quantity": 22,
    "direction": OrderSideType.Sell,
    "cost": 115,
    "time": datetime(2020, 9, 10, tzinfo=pytz.utc),
}
position_1 = {
    "security": Equity(asset_currency="USD", symbol="AAPL"),
    "orders": [order_1, order_2, order_3],
}
position_2 = {
    "security": Equity(asset_currency="CAD", symbol="RY.TO"),
    "orders": [order_4, order_5, order_6],
}
portfolio_1 = {
    "name": "portfolio_1",
    "portfolio_type": PortfolioType.margin,
    "reporting_currency": Currency("USD"),
    "benchmark": Index(asset_currency="USD", symbol="^GSPC"),
    "positions": [position_1, position_2],
}

user_1 = {
    "email": "tuncutku10@gmail.com",
    "password": "1234",
    "portfolios": [portfolio_1],
}


######## Market data ########

value_1 = SingleValue(55, Currency("USD"))
value_2 = SingleValue(10, Currency("USD"))
value_3 = SingleValue(-10, Currency("CAD"))

index_1 = IndexValue(
    Series(
        [10, 14, 20, 26],
        index=[
            date(2020, 1, 6),
            date(2020, 3, 2),
            date(2020, 5, 12),
            date(2020, 7, 2),
        ],
    ),
    Currency("USD"),
)
index_2 = IndexValue(
    Series(
        [20, 110, 40, 78],
        index=[
            date(2020, 1, 6),
            date(2020, 3, 30),
            date(2020, 5, 12),
            date(2020, 7, 30),
        ],
    ),
    Currency("USD"),
)
index_3 = IndexValue(Series([-15, 14, -56, 16]), Currency("CAD"))

mock_series = Series(
    [50, 51, 52, 53, 54, 55, 56],
    index=[
        date(2020, 1, 1),
        date(2020, 2, 1),
        date(2020, 3, 1),
        date(2020, 4, 1),
        date(2020, 5, 1),
        date(2020, 6, 1),
        date(2020, 7, 1),
    ],
)
