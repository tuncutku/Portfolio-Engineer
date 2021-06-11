"""Test alert objects."""

from collections import namedtuple
from datetime import date

import pytest

from src.environment import Portfolio
from src.market.signal import Signal, PortfolioValueSignal, DailyPortfolioReturnSignal
from src.market.ref_data import aapl, up

from tests.test_data import market as mkt

AlertResults = namedtuple(
    "AlertResults",
    ["target", "apply_operator", "str"],
)
signal_test_contents = [
    (
        mkt.price_signal,
        AlertResults(
            100, True, "Signal triggered when current price is upper than 100."
        ),
    ),
    (
        mkt.return_signal,
        AlertResults(
            0.02, False, "Signal triggered when daily return is upper than 2.00%."
        ),
    ),
    (
        mkt.limit_signal,
        AlertResults(
            0.05,
            True,
            "Signal triggered when the return calculated by max or min price from the starting date is upper than 5.00%.",
        ),
    ),
]
signal_test_names = [signal[0].__class__.__name__ for signal in signal_test_contents]


@pytest.mark.parametrize("signal, results", signal_test_contents, ids=signal_test_names)
def test_single_instrument_signals(
    mock_current_md, signal: Signal, results: AlertResults
):
    """Test price signal."""

    assert signal.underlying == aapl
    assert signal.creation_date == date.today()

    assert signal.operator == up
    assert isinstance(signal.value, float)
    assert signal.target == results.target
    assert str(signal) == results.str
    assert signal.apply_operator() == results.apply_operator

    assert signal.active is True
    signal.deactivate()
    assert signal.active is False
    signal.activate()
    assert signal.active is True


def test_portfolio_signals(client, _db, load_environment_data):
    """Test portfolio daily return signal."""

    port = Portfolio.find_by_id(1)
    port_return = DailyPortfolioReturnSignal(port, up, 0.05)
    port_value = PortfolioValueSignal(port, up, 100000)

    return_str = "Signal triggered when portfolio daily return is upper than 5.00%."
    value_str = "Signal triggered when portfolio current value is upper than 100000."

    for signal, string in zip((port_return, port_value), (return_str, value_str)):
        assert signal.underlying == port
        assert signal.creation_date == date.today()
        assert signal.operator == up
        assert isinstance(signal.value, float)
        assert signal.apply_operator() is False
        assert str(signal) == string
