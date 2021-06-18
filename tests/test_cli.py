"""Test CLI"""
# pylint: disable=unused-argument


from flask_sqlalchemy import inspect

from src.cli import seed_data, init_db, clear_db
from src.extensions import db

from src.environment import User, Portfolio, Position, Order


def get_table_names() -> list:
    """Get existing table names."""

    conn = db.engine.connect()
    inspector = inspect(conn)
    return inspector.get_table_names()


def test_cli(client):
    """Test registered flask CLIs."""

    runner = client.application.test_cli_runner()

    tables = get_table_names()
    assert not tables

    result = runner.invoke(init_db)
    assert result.exit_code == 0

    tables = get_table_names()
    assert tables == [
        "daily_report",
        "market_alert",
        "orders",
        "portfolios",
        "positions",
        "users",
    ]

    result = runner.invoke(seed_data)
    assert result.exit_code == 0

    for _object in [User, Portfolio, Position, Order]:
        assert len(_object.find_all()) == 1

    result = runner.invoke(clear_db)
    assert result.exit_code == 0

    tables = get_table_names()
    assert not tables
