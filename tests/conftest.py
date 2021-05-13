"""Test fixtures"""
# pylint: disable=redefined-outer-name, unused-argument

import pytest
from flask import template_rendered

from src import create_app
from src.environment.user import User
from src.extensions import db
from tests.test_data.sample_data import user_1


@pytest.fixture
def app():
    """Create application for the tests."""

    app = create_app("testing")
    return app


@pytest.fixture
def _db(client):
    """Create database for the tests."""

    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture
def test_user(client):
    """Provides sample user, portfolio, position and order."""

    _user = User(email=user_1["email"])
    _user.save_to_db()
    _user.set_password(user_1["password"])
    _user.confirm_user()

    for port in user_1["portfolios"]:
        _port = _user.add_portfolio(
            port["name"],
            port["portfolio_type"],
            port["reporting_currency"],
            port["benchmark"],
        )
        for position in port["positions"]:
            _position = _port.add_position(position["security"])
            for order in position["orders"]:
                _position.add_order(
                    order["quantity"], order["direction"], order["cost"], order["time"]
                )

    yield _user


@pytest.fixture
def login(client):
    """Log in test user for URL tests."""

    client.post(
        "/users/login", data=dict(email=user_1["email"], password=user_1["password"])
    )


@pytest.fixture
def captured_templates(app):
    """Capture templates used as during system tests."""

    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def mock_symbol(mocker):
    """Mock symbol methods."""

    mocker.patch(
        "src.market.basic.Symbol.info",
        new_callable=mocker.PropertyMock,
        return_value={"regularMarketPrice": 50},
    )

    # def mock_load(self, start, end):
    #     return mock_series

    # mocker.patch("src.market.basic.Symbol.index", mock_load)
