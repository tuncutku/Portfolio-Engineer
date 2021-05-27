"""Test alert objects."""

from collections import namedtuple
from datetime import date

import pytest

from src.market.ref_data import aapl
from src.market.alert import Signal, Up

from tests.test_data import market as mkt

AlertResults = namedtuple(
    "AlertResults", ["condition", "target", "expiry_check", "condition_check"]
)
signal_test_contents = [
    (mkt.price_signal, AlertResults(Up(100), 120.0, False, True)),
    (mkt.return_signal, AlertResults(Up(0.05), 0.28768, False, True)),
]
signal_test_names = [signal[0].__class__.__name__ for signal in signal_test_contents]


@pytest.mark.parametrize("signal, results", signal_test_contents, ids=signal_test_names)
def test_return_signal(mock_current_md, signal: Signal, results: AlertResults):
    """Test price signal."""

    assert signal.security == aapl
    assert signal.creation_date == date.today()

    assert signal.condition == results.condition
    assert signal.target == results.target

    assert signal.check_expiry() == results.expiry_check
    assert signal.check_condition() == results.condition_check
