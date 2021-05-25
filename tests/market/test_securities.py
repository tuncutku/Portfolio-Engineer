"""Test securities"""
# pylint: disable=unused-argument, no-self-use


from datetime import date
import pytest

from src.market import Equity, ETF, Currency, Symbol, Security, SingleValue, IndexValue
from src.market.ref_data import usd_ccy

start_date = date(2020, 1, 4)

currency = Currency("USD")
etf = ETF(currency, Symbol("PBW"))
equity = Equity(currency, Symbol("AAPL"))


@pytest.mark.parametrize(
    "security, symbol, security_type",
    [(etf, Symbol("PBW"), "ETF"), (equity, Symbol("AAPL"), "Equity")],
    ids=["ETF", "Equity"],
)
def test_common(security: Security, symbol: Symbol, security_type: str):
    """Test common securities."""

    assert security.asset_currency == currency
    assert security.symbol == symbol
    assert security.security_type == security_type

    assert isinstance(security.value, SingleValue)
    assert isinstance(security.index(start_date), IndexValue)


def test_etf():
    """Test ETF."""


def test_equity():
    """Test Equity."""
