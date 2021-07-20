"""Test basic objects"""
# pylint: disable=pointless-statement, unused-argument, no-self-use


from datetime import date
from pandas import DataFrame, Series, DatetimeIndex

import pytest

from src.market import Symbol, Info
from src.market.ref_data import usd_ccy, cad_ccy, usdcad

start_date = date(2020, 1, 2)
end_date = date(2021, 1, 4)


def test_currency():
    """Test currency."""

    date_index = usd_ccy.calender(start_date, end_date)

    assert str(usd_ccy) == "USD"
    assert isinstance(date_index, DatetimeIndex)
    assert date_index.max().date() == date(2021, 1, 4)
    assert date_index.min().date() == date(2020, 1, 2)


def test_fx():
    """Test fx index."""

    assert str(usdcad) == "USDCAD FX Index"
    assert usdcad.symbol == Symbol("USDCAD=X")
    assert usdcad.asset_currency == cad_ccy
    assert usdcad.numeraire_currency == usd_ccy

    assert usdcad.rate == pytest.approx(1.2, 1)
    fx_index = usdcad.index(start_date, end_date)
    assert isinstance(fx_index, Series)
    assert fx_index.sum() == pytest.approx(352.41761, 5)
    assert len(fx_index) == 263


def test_symbol():
    """Test symbol."""

    symbol = Symbol("AAPL")
    wrong_symbol = Symbol("1111111111111")

    with pytest.raises(ValueError):
        symbol == ["AAPL"]

    assert str(symbol) == "AAPL"
    assert symbol == "AAPL"
    assert symbol.is_valid
    assert not wrong_symbol.is_valid
    assert isinstance(symbol.info, DataFrame)
    assert isinstance(symbol.get_info(Info.price), float)
    assert isinstance(symbol.index(date(2020, 1, 1), date.today()), Series)
    assert isinstance(symbol.indices(date(2020, 1, 1), date.today()), DataFrame)
    assert symbol.is_trading_day(date(2020, 1, 3))
    assert not symbol.is_trading_day(date(2020, 1, 1))
