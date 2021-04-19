# pylint: disable=redefined-outer-name, unused-argument

from collections import namedtuple
import pytest

from flask import template_rendered

from src.environment.user import User
from src import create_app
from src.extensions import db
from tests.sample_data import user_1, portfolio_1, position_1, order_1_1


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
def test_data(client):
    """Provides sample user, portfolio, position and order."""

    _user = User(email=user_1.get("email"))
    _user.save_to_db()
    _user.set_password(user_1.get("password"))
    _user.confirm_user()

    _port = _user.add_portfolio(**portfolio_1)
    _pos = _port.add_position(**position_1)
    _order = _pos.add_order(**order_1_1)

    test_data = namedtuple("test_data", ["user", "portfolio", "position", "order"])

    yield test_data(_user, _port, _pos, _order)


@pytest.fixture
def login(client, test_data):
    """Log in test user for URL tests."""

    client.post("/users/login", data=dict(**user_1))


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