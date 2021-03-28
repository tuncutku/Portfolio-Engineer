import pytest
import pytest_flask

from flask import template_rendered

from src import create_app
from src.extensions import db as _db
from tests.sample_data import *
from tests.utils import *


@pytest.fixture
def app():
    """Create application for the tests."""

    app = create_app("config.TestConfig")
    return app


@pytest.fixture
def db(client):
    """Create database for the tests."""

    _db.create_all()
    yield _db
    _db.session.remove()
    _db.drop_all()


@pytest.fixture
def user(client):
    """Log in test user for URL tests."""
    user_test = create_user(**user_1)
    portfolio_test = create_portfolio(**portfolio_1, user=user_test)
    position_test = create_position(**position_1, portfolio=portfolio_test)
    order_test = create_order(**order_1, position=position_test)

    client.post("/users/login", data=dict(**user_1))

    yield user_test


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)