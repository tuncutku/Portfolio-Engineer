from datetime import datetime
from src.environment.user_activities.portfolio import PortfolioType, Currency
from src.environment.user_activities.order import OrderSideType, SecurityType


user_1 = {"email": "tuncutku@gmail.com", "password": "1234"}
portfolio_1 = {
    "name": "portfolio_1",
    "portfolio_type": PortfolioType.margin,
    "reporting_currency": Currency.USD,
}
portfolio_2 = {
    "name": "portfolio_2",
    "portfolio_type": PortfolioType.cash,
    "reporting_currency": Currency.CAD,
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
    "exec_time": datetime.now(),
    "fee": 0.123,
}
order_2 = {
    "symbol": "AAPL",
    "quantity": 2,
    "side": OrderSideType.Sell,
    "avg_exec_price": 11,
    "exec_time": datetime.now(),
    "fee": 0,
}
