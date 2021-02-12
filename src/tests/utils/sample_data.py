from datetime import datetime

user_1 = {"email": "tuncutku@gmail.com", "password": "1234"}
portfolio_1 = {
    "name": "portfolio_1",
    "portfolio_type": "invalid",
    "reporting_currency": "CAD",
}
portfolio_2 = {
    "name": "portfolio_2",
    "portfolio_type": "TFSA",
    "reporting_currency": "USD",
}
position_1 = {
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "security_type": "Equity",
    "currency": "USD",
}
position_2 = {
    "symbol": "FB",
    "name": "Facebook Inc.",
    "security_type": "Equity",
    "currency": "USD",
}
order_1 = {
    "symbol": "AAPL",
    "quantity": "1",
    "side": "Buy",
    "avg_exec_price": 10.5,
    "exec_time": datetime.now(),
    "fee": 0.123,
}
order_2 = {
    "symbol": "AAPL",
    "quantity": "2",
    "side": "Sell",
    "avg_exec_price": 11,
    "exec_time": datetime.now(),
    "fee": 0,
}