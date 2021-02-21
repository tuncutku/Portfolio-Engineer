from datetime import datetime
from src.environment.portfolio import PortfolioType, Currency
from src.environment.order import OrderSideType, SecurityType


user_1 = {"email": "test_user@gmail.com", "password": "1234"}
portfolio_1 = {
    "name": "portfolio_1",
    "portfolio_type": PortfolioType.margin,
    "reporting_currency": Currency.USD,
    "date": datetime(2020, 1, 1),
}
portfolio_2 = {
    "name": "portfolio_2",
    "portfolio_type": PortfolioType.cash,
    "reporting_currency": Currency.CAD,
    "date": datetime(2020, 1, 1),
}
position_1 = {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "security_type": SecurityType.Stock,
    "currency": Currency.USD,
}
position_2 = {
    "symbol": "FB",
    "name": "Facebook Inc.",
    "security_type": SecurityType.Stock,
    "currency": Currency.USD,
}
order_1 = {
    "symbol": "AAPL",
    "quantity": 10,
    "side": OrderSideType.Buy,
    "avg_exec_price": 10.5,
    "exec_time": datetime(2020, 1, 1, 1, 1),
    "fee": 0.123,
}
order_2 = {
    "symbol": "AAPL",
    "quantity": 2,
    "side": OrderSideType.Sell,
    "avg_exec_price": 11,
    "exec_time": datetime(2020, 4, 6, 5, 30),
    "fee": 0,
}
