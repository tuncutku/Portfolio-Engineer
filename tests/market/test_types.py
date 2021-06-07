"""Test types"""

from src.market.ref_data import buy, sell


def test_direction():
    """Test direction."""

    assert str(buy) == "Buy"
    assert str(sell) == "Sell"

    assert buy * 100 == 100
    assert sell * 100 == -100
