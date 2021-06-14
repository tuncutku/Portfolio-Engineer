"""Test portfolio object"""
# pylint: disable=unused-argument

from datetime import date

from src.environment import User, Portfolio
from src.market import Symbol, Equity, ETF
from src.market.ref_data import usd_ccy, cad_ccy, gspc, aapl
from src.market.types import PortfolioType
from tests.test_data import environment as env


start_date = date(2020, 5, 4)
end_date = date(2020, 5, 20)


def test_portfolio_object(client, _db, load_environment_data):
    """Test saved portfolio object."""

    port = Portfolio.find_by_id(1)

    assert port == Portfolio.find_by_id(1)
    assert port.id == 1
    assert port.name == env.portfolio_1_raw["name"]
    assert port.portfolio_type == PortfolioType.tfsa
    assert port.reporting_currency == cad_ccy
    assert port.benchmark == gspc
    assert not port.primary
    assert port.daily_report.active is True
    assert isinstance(port.date, date)
    assert repr(port) == "<Portfolio portfolio_1.>"


def test_portfolio_primary(client, _db, load_environment_data):
    """Test portfolio primary method."""

    user = User.find_by_id(1)
    port = Portfolio.find_by_id(1)

    assert port.primary is False
    port.set_as_primary()
    assert port.primary is True
    assert port == user.get_primary_portfolio()


def test_portfolio_edit(client, _db, load_environment_data):
    """Test portfolio edit method."""

    port = Portfolio.find_by_id(1)

    port.edit("Hello World", usd_ccy, PortfolioType.rrsp, aapl)
    assert port.name == "Hello World"
    assert port.reporting_currency == usd_ccy
    assert port.portfolio_type == PortfolioType.rrsp
    assert port.benchmark == aapl


def test_portfolio_get_methods(client, _db, load_environment_data):
    """Test portfolio get position methods."""

    user = User.find_by_id(1)
    port = Portfolio.find_by_id(1)

    assert port.get_position_by_symbol(Symbol("AAPL"))
    assert port.get_position_by_symbol(Symbol("AAP")) is None
    assert len(port.get_positions_by_security_type(Equity)) == 2
    assert len(port.get_positions_by_security_type(ETF)) == 0
    assert len(port.get_open_positions()) == 2
    assert port == user.get_portfolio_by_name("portfolio_1")


def test_portfolio_values(client, _db, load_environment_data, mock_current_md):
    """Test portfolio values."""

    port = Portfolio.find_by_id(1)

    # Current value
    cad_value = port.current_value()
    usd_value = port.current_value(usd_ccy)
    assert cad_value.value > usd_value.value
    # Historal value
    port_values = port.historical_value(start_date, end_date)
    assert port_values == env.portfolio_values_index
    port_values_usd = port.historical_value(start_date, end_date, usd_ccy)
    assert port_values_usd == env.portfolio_values_usd_index
    # Instrument values
    security_values = port.security_values(start_date, end_date)
    assert security_values.equals(env.portfolio_position_values_df)
    security_values_cad = port.security_values(start_date, end_date, cad_ccy)
    assert security_values_cad.equals(env.portfolio_position_values_cad_df)


def test_portfolio_quantities(client, _db, load_environment_data):
    """Test portfolio quantities."""

    port = Portfolio.find_by_id(1)

    quantities = port.position_quantities(date(2020, 1, 4), date(2021, 5, 23))
    assert quantities.equals(env.portfolio_quantities_df)
