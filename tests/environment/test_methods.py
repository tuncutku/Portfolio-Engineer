"""Test environment object methods."""

from datetime import date, datetime
from pandas import Series
from pytest import approx

from src.environment.portfolio import Portfolio
from src.environment.utils.types import OrderSideType, PortfolioType
from src.market import Currency, SingleValue, IndexValue, Symbol, Equity, ETF
from src.environment import User, Portfolio, Position, Order
from tests.sample_data import user_1
from tests.raw_data.portfolio import portfolio_index
from tests.raw_data.position import position_index

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
    assert port.benchmark == "^GSPC"

    assert port.current_value == SingleValue(-14600, cad)
    assert isinstance(port.historical_value(start_date, end_date), IndexValue)
    # assert port.historical_value(start_date, end_date) == approx(
    #     IndexValue(Series(portfolio_index), cad)
    # )

    # Test get positions
    assert port.get_position_by_symbol(Symbol("AAPL"))
    assert port.get_position_by_symbol(Symbol("AAP")) is None
    assert len(port.get_positions_by_security(Equity)) == 2
    assert len(port.get_positions_by_security(ETF)) == 0


def test_position(client, _db, test_user, mock_symbol):
    """Unit test for position methods."""

    pos = Position.find_by_id(1)

    assert pos.is_open
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
    assert pos.current_value() == SingleValue(-300, usd)
    assert pos.current_value(cad) == SingleValue(-15000, cad)
    # assert pos.historical_value(cad, start_date, end_date) == IndexValue(
    #     Series(position_index), cad
    # )
    assert isinstance(pos.historical_value(cad, start_date, end_date), IndexValue)


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
