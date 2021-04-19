from datetime import datetime
import pytz

from src.environment.portfolio import PortfolioType
from src.environment.order import OrderSideType

from src.market import Currency, Symbol, Equity


user_1 = {"email": "tuncutku10@gmail.com", "password": "1234"}
portfolio_1 = {
    "name": "portfolio_1",
    "portfolio_type": PortfolioType.margin,
    "reporting_currency": Currency("USD"),
    "benchmark": Symbol("^GSPC"),
}
portfolio_2 = {
    "name": "portfolio_2",
    "portfolio_type": PortfolioType.cash,
    "reporting_currency": Currency("CAD"),
    "benchmark": Symbol("^GSPC"),
}
position_1 = {
    "security": Equity(asset_currency="USD", symbol="AAPL"),
}
position_2 = {
    "security": Equity(asset_currency="USD", symbol="FB"),
}

order_1_1 = {
    "quantity": 10,
    "direction": OrderSideType.Buy,
    "price": 10.5,
    "time": datetime(2020, 1, 3, tzinfo=pytz.utc),
    "fee": 0.123,
}
order_1_2 = {
    "quantity": 2,
    "direction": OrderSideType.Sell,
    "price": 11,
    "time": datetime(2020, 4, 6, tzinfo=pytz.utc),
    "fee": 0,
}
order_2 = {
    "quantity": 20,
    "side": OrderSideType.Buy,
    "exec_price": 11,
    "exec_time": datetime(2020, 8, 6, tzinfo=pytz.utc),
    "fee": 0,
}
