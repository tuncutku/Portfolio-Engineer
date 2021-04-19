from datetime import date
from pytest import approx

from src.market import FX, Cash, Currency, IndexValue, SingleValue, Symbol

start_date = date(2020, 2, 3)


def test_fx():
    """Test fx index."""

    usdcad = FX(asset_currency="CAD", numeraire_currency="USD")
    assert str(usdcad) == "USDCAD"
    assert usdcad.symbol == Symbol("USDCAD=X")
    assert usdcad.asset_currency == Currency("CAD")
    assert usdcad.numeraire_currency == Currency("USD")

    fx_value = usdcad.value
    assert isinstance(fx_value, SingleValue)
    assert isinstance(fx_value.value, float)
    assert fx_value.currency == Currency("USD")

    fx_index = usdcad.index(start_date)

    assert isinstance(fx_index, IndexValue)
    assert fx_index.currency == Currency("CAD")
    assert fx_index.index.index.min().date() == date(2020, 2, 3)
    assert fx_index.index.min() == approx(1.235, 3)


def test_cash():
    """Test cash."""

    cash = Cash(asset_currency="USD")
    assert repr(cash) == "<Cash in USD.>"
    assert cash.asset_currency == Currency("USD")
    assert cash.value == SingleValue(1, Currency("USD"))
    cash.index(start_date)