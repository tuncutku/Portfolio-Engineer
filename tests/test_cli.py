"""Test CLI"""
# pylint: disable=unused-argument

from flask.testing import FlaskCliRunner
from flask_sqlalchemy import inspect

from click import testing
from src.cli import seed_data, init_db, clear_db, list_users, add_user
from src.extensions import db
from src.environment import User, Portfolio, Position, Order


def get_table_names() -> list:
    """Get existing table names."""

    conn = db.engine.connect()
    inspector = inspect(conn)
    return inspector.get_table_names()


def test_db(client, runner: FlaskCliRunner):
    """Test registered database CLIs."""

    tables = get_table_names()
    assert not tables

    result: testing.Result = runner.invoke(init_db)
    assert result.exit_code == 0
    assert result.output == "Initializing database.\nTask completed.\n"

    tables = get_table_names()
    assert tables == [
        "daily_report",
        "market_alerts",
        "orders",
        "portfolios",
        "positions",
        "users",
        "watchlist_instruments",
    ]

    result: testing.Result = runner.invoke(seed_data)
    assert result.exit_code == 0
    assert (
        result.output == ""
        "Database created.\nSample objects added into the database.\nTask completed.\n"
        ""
    )

    for _object in [User, Portfolio, Position, Order]:
        assert len(_object.find_all()) == 1

    result: testing.Result = runner.invoke(clear_db)
    assert result.exit_code == 0
    assert result.output == "Dropping database.\nTask completed.\n"

    tables = get_table_names()
    assert not tables


def test_list_users(client, _db, load_environment_data, runner: FlaskCliRunner):
    """Test list users cli."""

    result: testing.Result = runner.invoke(list_users)
    assert result.exit_code == 0
    assert result.output == "User: tuncutku10@gmail.com --> number of portfolios: 1\n"


def test_add_user(client, _db, runner: FlaskCliRunner):
    """Test list users cli."""

    assert not User.find_all()

    result: testing.Result = runner.invoke(add_user, input="tuncutku@gmail.com\n1234\n")
    assert result.exit_code == 0
    assert (
        "User with the email: tuncutku@gmail.com added in to the database."
        in result.output
    )
    result: testing.Result = runner.invoke(add_user, input="tuncutku@gmail.com\n1234\n")
    assert result.exit_code == 2
    assert "Invalid value: Email already exists in the database." in result.output
