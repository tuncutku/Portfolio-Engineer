"""Test environment object methods"""
# pylint: disable=unused-argument

from datetime import date, datetime
from pandas import Series
from pytest import approx

from src.market.types import OrderSideType, PortfolioType
from src.market import Currency, SingleValue, IndexValue, Symbol, Equity, ETF
from src.environment import User, Portfolio, Position, Order, DailyReport
from tests.sample_data import user_1

start_date = date(2020, 1, 1)
end_date = date(2021, 1, 1)
cad = Currency("CAD")
usd = Currency("USD")


def test_user(client, _db, test_user):
    """Unit test for user methods."""

    assert test_user == User.find_by_email(user_1["email"])
    assert test_user.check_password(user_1["password"]) is True


def test_portfolio(client, _db, test_user, mock_symbol):
    """Unit test for portfolio methods."""

    port = test_user.portfolios[0]

    # Test primary attribute
    assert port.primary is False
    port.set_as_primary()
    assert port.primary is True
    assert port == Portfolio.get_primary(test_user)

    # Test edit portfolio attribute
    port.edit("Hello World", Currency("CAD"), PortfolioType.rrsp, "^GSPC")
    assert port.name == "Hello World"
    assert port.reporting_currency == Currency("CAD")
    assert port.portfolio_type == PortfolioType.rrsp
    assert port.benchmark == Symbol("^GSPC")
    assert port.current_value == SingleValue(-14600, cad)

    # Test portfolio historical value
    port_values = port.historical_value(start_date, end_date)
    assert isinstance(port_values, IndexValue)
    assert port_values.currency == Currency(("CAD"))
    assert len(port_values.index) == 261
    assert port_values.index.sum() == approx(704496.162754139, 5)

    # Test get positions
    assert port.get_position_by_symbol(Symbol("AAPL"))
    assert port.get_position_by_symbol(Symbol("AAP")) is None
    assert len(port.get_positions_by_security(Equity)) == 2
    assert len(port.get_positions_by_security(ETF)) == 0


def test_position(client, _db, test_user, mock_symbol):
    """Unit test for position methods."""

    pos = Position.find_by_id(1)
    assert pos.is_open

    # Test cumulative quantity
    cum_quantity = pos.cumulative_quantity
    assert isinstance(cum_quantity, Series)
    assert len(cum_quantity) == 331
    assert cum_quantity.sum() == 1686.0

    assert Series.equals(
        pos.quantity,
        Series(
            [10, -2, -14],
            index=[date(2020, 2, 3), date(2020, 7, 1), date(2021, 1, 13)],
        ),
    )
    assert Series.equals(
        pos.cost,
        Series(
            [130.0, 122.0, 126.0],
            index=[date(2020, 2, 3), date(2020, 7, 1), date(2021, 1, 13)],
        ),
    )

    # Test current value
    assert pos.current_value() == SingleValue(-300, usd)
    assert pos.current_value(cad) == SingleValue(-15000, cad)

    # Test position historical value
    position_hist_value = pos.historical_value(cad, start_date, end_date)
    assert isinstance(position_hist_value, IndexValue)
    assert position_hist_value.currency == Currency("CAD")
    assert len(position_hist_value.index) == 239
    assert position_hist_value.index.sum() == approx(269076.5134, 5)


def test_order(client, _db, test_user):
    """Unit test for order methods."""

    order = Order.find_by_id(2)

    assert order.adjusted_quantity == -2
    assert Series.equals(order.cost_df, Series([122.0], index=[date(2020, 7, 1)]))
    assert Series.equals(order.quantity_df, Series([-2], index=[date(2020, 7, 1)]))

    # Edit Order
    order.edit(20, OrderSideType.Buy, 100, datetime(2020, 1, 1))
    assert order.quantity == 20
    assert order.direction == OrderSideType.Buy
    assert order.cost == 100
    assert order.time == datetime(2020, 1, 1)


def test_daily_alert(client, _db, test_user):
    """Unit test for daily alert methods."""

    daily_alert = DailyReport.find_by_id(1)
    assert daily_alert.condition
    assert daily_alert.email_template == "email/daily_report.html"
    assert daily_alert.recipients == user_1["email"]

    content = daily_alert.generate_email_content()
