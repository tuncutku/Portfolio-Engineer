"""Test environment object relations"""
# pylint: disable=unused-argument, pointless-statement

import pytest
from src.environment import (
    User,
    Portfolio,
    Position,
    Order,
    DailyReport,
    MarketAlert,
    Alert,
    WatchListInstrument,
)


classes = [User, Portfolio, Position, Order]


def test_relationships(client, _db, load_environment_data):
    """Integration test for model relationships."""

    user = User.find_by_id(1)
    user.delete_from_db()
    for _object in [
        User,
        Portfolio,
        Position,
        Order,
        MarketAlert,
        WatchListInstrument,
        DailyReport,
    ]:
        assert not _object.find_all()


def test_object_number(client, _db, load_environment_data):
    """Test saved test objects."""

    assert len(User.find_all()) == 1
    assert len(Portfolio.find_all()) == 1
    assert len(Position.find_all()) == 2
    assert len(Order.find_all()) == 6
    assert len(DailyReport.find_all()) == 1
    assert len(MarketAlert.find_all()) == 1
    assert len(WatchListInstrument.find_all()) == 1


def test_base_model(client, _db):
    """Test base object."""

    alert_base = Alert()

    with pytest.raises(NotImplementedError):
        alert_base.recipients

    with pytest.raises(NotImplementedError):
        alert_base.subject

    with pytest.raises(NotImplementedError):
        alert_base.email_template

    with pytest.raises(NotImplementedError):
        alert_base.condition()

    with pytest.raises(NotImplementedError):
        alert_base.generate_email_content()
