"""Test alert objects."""

from collections import namedtuple
from datetime import date

import pytest

from src.market.signal import Signal
from src.market.ref_data import aapl, up

from tests.test_data import market as mkt

AlertResults = namedtuple(
    "AlertResults",
    ["operator", "value", "target", "check_expiry", "apply_operator", "str"],
)
signal_test_contents = [
    (
        mkt.price_signal,
        AlertResults(
            up,
            120,
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
            0.28768,
            0.02,
            False,
            True,
            "Signal triggered when return is upper than 2.00%.",
        ),
    ),
]
signal_test_names = [signal[0].__class__.__name__ for signal in signal_test_contents]


@pytest.mark.parametrize("signal, results", signal_test_contents, ids=signal_test_names)
def test_signals(mock_current_md, signal: Signal, results: AlertResults):
    """Test price signal."""

    assert signal.security == aapl
    assert signal.creation_date == date.today()

    assert signal.operator == results.operator
    assert signal.value == results.value
    assert signal.target == results.target
    assert str(signal) == results.str

    assert signal.check_expiry() == results.check_expiry
    assert signal.apply_operator() == results.apply_operator
