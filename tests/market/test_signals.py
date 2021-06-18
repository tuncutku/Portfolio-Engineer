"""Test alert objects."""
# pylint: disable=unused-argument, line-too-long, invalid-name

from datetime import date

import pytest

from src.environment import Portfolio
from src.market.signal import Signal, PortfolioValueSignal, DailyPortfolioReturnSignal
from src.market.ref_data import aapl, up, up_equal, down, down_equal

from tests.test_data import market as mkt


price_signal_str = "Signal triggered when current price is upper than 100."
return_signal_str = "Signal triggered when daily return is upper than 10.00%."
limit_signal_str = "Signal triggered when the return calculated by max or min price from the starting date is upper than 10.00%."


signal_test_contents = [
    (mkt.price_signal, 100, True, price_signal_str),
    (mkt.return_signal, 0.1, False, return_signal_str),
    (mkt.limit_signal, 0.1, True, limit_signal_str),
    (mkt.limit_signal_default, 0.1, False, limit_signal_str),
]
signal_test_names = [signal[0].__class__.__name__ for signal in signal_test_contents]


@pytest.mark.parametrize(
    "signal, target, apply_operator, string",
    signal_test_contents,
    ids=signal_test_names,
)
def test_single_instrument_signals(
    mock_current_md, signal: Signal, target: float, apply_operator: bool, string: str
):
    """Test price signal."""

    assert signal.underlying == aapl
    assert signal.creation_date == date.today()

    assert signal.operator == up
    assert isinstance(signal.value, float)
    assert signal.target == target
    assert str(signal) == string
    assert signal.apply_operator() == apply_operator


def test_portfolio_signals(client, _db, load_environment_data, login):
    """Test portfolio daily return signal."""

    port = Portfolio.find_by_id(1)
    port_return = DailyPortfolioReturnSignal(port.name, up, 0.05)
    port_value = PortfolioValueSignal(port.name, up, 100000)

    return_str = "Signal triggered when portfolio daily return is upper than 5.00%."
    value_str = "Signal triggered when portfolio current value is upper than 100000."

    for signal, string in zip((port_return, port_value), (return_str, value_str)):
        assert signal.underlying == port.name
        assert signal.creation_date == date.today()
        assert signal.operator == up
        assert isinstance(signal.value, float)
        assert signal.apply_operator() is False
        assert str(signal) == string


def test_operators():
    """Test operators."""

    for operator, string in zip(
        (up, up_equal, down, down_equal),
        ("upper", "upper or equal", "lower", "lower or equal"),
    ):
        assert str(operator) == string
