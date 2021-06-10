"""Test alert objects."""

from collections import namedtuple
from datetime import date

import pytest

from src.market.signal import Signal
from src.market.ref_data import aapl, up

from tests.test_data import market as mkt

AlertResults = namedtuple(
    "AlertResults",
    ["operator", "target", "check_expiry", "apply_operator", "str"],
)
signal_test_contents = [
    (
        mkt.price_signal,
        AlertResults(
            up,
            100,
            False,
            True,
            "Signal triggered when current price is upper than 100.",
        ),
    ),
    (
        mkt.return_signal,
        AlertResults(
            up,
            0.02,
            False,
            False,
            "Signal triggered when daily return is upper than 2.00%.",
        ),
    ),
    (
        mkt.limit_signal,
        AlertResults(
            up,
            0.05,
            False,
            False,
            "Signal triggered when the return calculated by max or min price from the starting date is upper than 5.00%.",
        ),
    ),
]
signal_test_names = [signal[0].__class__.__name__ for signal in signal_test_contents]


@pytest.mark.parametrize("signal, results", signal_test_contents, ids=signal_test_names)
def test_signals(mock_current_md, signal: Signal, results: AlertResults):
    """Test price signal."""

    assert signal.underlying == aapl
    assert signal.creation_date == date.today()

    assert signal.operator == results.operator
    assert isinstance(signal.value, float)
    assert signal.target == results.target
    assert str(signal) == results.str
    assert signal.apply_operator() == results.apply_operator

    assert signal.active is True
    signal.deactivate()
    assert signal.active is False
    signal.activate()
    assert signal.active is True
