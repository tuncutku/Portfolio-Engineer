"""Sample request data"""

from datetime import date, datetime

start_date = date(2020, 1, 2).strftime("%Y-%m-%d")

required_field = ["This field is required."]
invalid_email = ["Invalid email address."]
invalid_password = ["Invalid email, password or account has not been confirmed yet."]
invalid_password_confirmation = ["Field must be equal to password."]
short_password = ["Field must be at least 4 characters long."]
user_exists = ["User with tuncutku10@gmail.com email address already exists."]
portfolio_exists = ["Portfolio with the name portfolio_1 already exists."]
long_name = ["Field cannot be longer than 20 characters."]
invalid_ticker = ["Invalid Ticker!"]
future_date = ["Can not accept a future date!"]
positive_input = ["Input should be 0 or more!"]
ticker_location = ["Only US and Canadian securities are supported!"]
invalid_trading_day = ["Given date is not a trading day."]
invalid_portfolio_name = ["Portfolio name is not valid!"]
missing_alert_date = ["Date must be provided when signal is limit signal!"]

user_login_data = [
    (
        dict(email="tuncutku10@gmail.com", password="1234"),
        dict(email=None, password=None),
        True,
    ),
    (
        dict(email="tuncutku10@gmail.com", password="12345"),
        dict(email=None, password=invalid_password),
        False,
    ),
    (
        dict(email=None, password=None),
        dict(email=required_field, password=required_field),
        False,
    ),
]

user_register_data = [
    (
        dict(email="tuncutku@gmail.com", password="1234", confirm="1234"),
        dict(email=None, password=None, confirm=None),
        True,
    ),
    (
        dict(email="tuncutku10@gmail.com", password="1234", confirm="123"),
        dict(email=user_exists, password=None, confirm=invalid_password_confirmation),
        False,
    ),
    (
        dict(email="tuncutku10", password="123", confirm="123"),
        dict(email=invalid_email, password=short_password, confirm=None),
        False,
    ),
    (
        dict(email=None, password=None, confirm=None),
        dict(email=required_field, password=required_field, confirm=required_field),
        False,
    ),
]

add_portfolio_data = [
    (
        dict(
            port_name="Port",
            port_type="Cash",
            reporting_currency="CAD",
            benchmark="^GSPC",
        ),
        dict(port_name=None, port_type=None, reporting_currency=None, benchmark=None),
        True,
    ),
    (
        dict(
            port_name="PortPortPortPortPortPortPortPortPortPort",
            port_type="Cash",
            reporting_currency="CAD",
            benchmark=None,
        ),
        dict(
            port_name=long_name,
            port_type=None,
            reporting_currency=None,
            benchmark=required_field,
        ),
        False,
    ),
    (
        dict(
            port_name="portfolio_1",
            port_type="Cash",
            reporting_currency="CAD",
            benchmark="portfolio_1portfolio_1portfolio_1",
        ),
        dict(
            port_name=portfolio_exists,
            port_type=None,
            reporting_currency=None,
            benchmark=invalid_ticker,
        ),
        False,
    ),
    (
        dict(
            port_name=None,
            port_type="Cash",
            reporting_currency="CAD",
            benchmark="^GSPC",
        ),
        dict(
            port_name=required_field,
            port_type=None,
            reporting_currency=None,
            benchmark=None,
        ),
        False,
    ),
]

edit_portfolio_data = [
    (
        dict(
            port_name="portfolio_1",
            port_type="Cash",
            reporting_currency="CAD",
            benchmark="^GSPC",
        ),
        dict(port_name=None, port_type=None, reporting_currency=None, benchmark=None),
        True,
    ),
    (
        dict(
            port_name="PortPortPortPortPortPortPortPortPortPort",
            port_type="Cash",
            reporting_currency="CAD",
            benchmark=None,
        ),
        dict(
            port_name=long_name,
            port_type=None,
            reporting_currency=None,
            benchmark=required_field,
        ),
        False,
    ),
    (
        dict(
            port_name=None,
            port_type="Cash",
            reporting_currency="CAD",
            benchmark="^GSPC",
        ),
        dict(
            port_name=required_field,
            port_type=None,
            reporting_currency=None,
            benchmark=None,
        ),
        False,
    ),
]

add_order_data = [
    (
        dict(
            symbol="AAPL",
            quantity=20,
            direction="Buy",
            cost=60,
            exec_datetime=datetime(2020, 1, 2),
        ),
        dict(
            symbol=None,
            quantity=None,
            direction=None,
            cost=None,
            exec_datetime=None,
        ),
        True,
    ),
    (
        dict(
            symbol=None,
            quantity=None,
            direction="Buy",
            cost=None,
            exec_datetime=None,
        ),
        dict(
            symbol=required_field,
            quantity=required_field,
            direction=None,
            cost=required_field,
            exec_datetime=required_field,
        ),
        False,
    ),
    (
        dict(
            symbol="NoneNoneNone",
            quantity=-20,
            direction="Buy",
            cost=-20,
            exec_datetime=datetime(2027, 1, 2),
        ),
        dict(
            symbol=invalid_ticker,
            quantity=positive_input,
            direction=None,
            cost=positive_input,
            exec_datetime=future_date,
        ),
        False,
    ),
    (
        dict(
            symbol="THYAO.IS",
            quantity=20,
            direction="Buy",
            cost=60,
            exec_datetime=datetime(2020, 1, 1),
        ),
        dict(
            symbol=ticker_location,
            quantity=None,
            direction=None,
            cost=None,
            exec_datetime=invalid_trading_day,
        ),
        False,
    ),
]

edit_order_data = [
    (
        dict(
            symbol="AAPL",
            quantity=20,
            direction="Buy",
            cost=60,
            exec_datetime=datetime(2020, 1, 2),
        ),
        dict(
            symbol=None,
            quantity=None,
            direction=None,
            cost=None,
            exec_datetime=None,
        ),
        True,
    ),
    (
        dict(
            symbol="AAPL",
            quantity=None,
            direction="Buy",
            cost=None,
            exec_datetime=None,
        ),
        dict(
            symbol=None,
            quantity=required_field,
            direction=None,
            cost=required_field,
            exec_datetime=required_field,
        ),
        False,
    ),
    (
        dict(
            symbol="AAPL",
            quantity=-20,
            direction="Buy",
            cost=-20,
            exec_datetime=datetime(2027, 1, 2),
        ),
        dict(
            symbol=None,
            quantity=positive_input,
            direction=None,
            cost=positive_input,
            exec_datetime=future_date,
        ),
        False,
    ),
    (
        dict(
            symbol="AAPL",
            quantity=20,
            direction="Buy",
            cost=60,
            exec_datetime=datetime(2020, 1, 1),
        ),
        dict(
            symbol=None,
            quantity=None,
            direction=None,
            cost=None,
            exec_datetime=invalid_trading_day,
        ),
        False,
    ),
]

add_alert_data = [
    (
        dict(signal="Price Signal", underlying="AAPL", operator="Up", target=130),
        dict(signal=None, underlying=None, operator=None, target=None),
        True,
    ),
    (
        dict(
            signal="Daily Return Signal", underlying="AAPL", operator="Up", target=0.05
        ),
        dict(signal=None, underlying=None, operator=None, target=None),
        True,
    ),
    (
        dict(
            signal="Limit Return Signal",
            underlying="AAPL",
            operator="Up",
            target=0.05,
            start_date=datetime(2020, 1, 2),
        ),
        dict(signal=None, underlying=None, operator=None, target=None),
        True,
    ),
    (
        dict(
            signal="Portfolio Value Signal",
            underlying="portfolio_1",
            operator="Up",
            target=1300,
        ),
        dict(signal=None, underlying=None, operator=None, target=None),
        True,
    ),
    (
        dict(
            signal="Daily Portfolio Return Signal",
            underlying="portfolio_1",
            operator="Up",
            target=0.05,
        ),
        dict(signal=None, underlying=None, operator=None, target=None),
        True,
    ),
    (
        dict(signal="Price Signal", underlying=None, operator="Up", target=None),
        dict(
            signal=None, underlying=required_field, operator=None, target=required_field
        ),
        False,
    ),
    (
        dict(
            signal="Limit Return Signal",
            underlying=None,
            operator="Up",
            target=None,
            start_date=None,
        ),
        dict(
            signal=None,
            underlying=required_field,
            operator=None,
            target=required_field,
            start_date=missing_alert_date,
        ),
        False,
    ),
    (
        dict(
            signal="Price Signal", underlying="portfolio_1", operator="Up", target=100
        ),
        dict(signal=None, underlying=invalid_ticker, operator=None, target=None),
        False,
    ),
    (
        dict(
            signal="Portfolio Value Signal",
            underlying="AAPL",
            operator="Up",
            target=100,
            start_date=datetime(2027, 1, 2),
        ),
        dict(
            signal=None,
            underlying=invalid_portfolio_name,
            operator=None,
            target=None,
            start_date=future_date,
        ),
        False,
    ),
]
