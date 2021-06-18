"""Test securities"""
# pylint: disable=unused-argument, no-self-use


from datetime import date
import pytest

from src.market import (
    Equity,
    ETF,
    Currency,
    Symbol,
    Instrument,
    SingleValue,
    IndexValue,
)

start_date = date(2020, 1, 4)

currency = Currency("USD")
etf = ETF(currency, Symbol("PBW"))
equity = Equity(currency, Symbol("AAPL"))


@pytest.mark.parametrize(
    "instrument, symbol, security_type, string",
    [
        (etf, Symbol("PBW"), "ETF", "ETF PBW"),
        (equity, Symbol("AAPL"), "Equity", "Equity AAPL"),
    ],
    ids=["ETF", "Equity"],
)
def test_common(
    instrument: Instrument, symbol: Symbol, security_type: str, string: str
):
    """Test common securities."""

    assert instrument.asset_currency == currency
    assert instrument.symbol == symbol
    assert instrument.security_type == security_type

    assert str(instrument) == string
    assert isinstance(instrument.name, str)
    assert isinstance(instrument.value(), SingleValue)
    assert isinstance(instrument.value(raw=True), float)
    assert isinstance(instrument.index(start_date), IndexValue)


def test_etf():
    """Test ETF."""


def test_equity():
    """Test Equity."""
