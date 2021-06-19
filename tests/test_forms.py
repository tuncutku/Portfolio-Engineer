"""Test forms"""
# pylint: disable=unused-argument, no-member, too-many-arguments

import pytest
from flask_wtf import FlaskForm

from tests.test_data import request
from src.environment import Portfolio, Order
from src.forms import (
    LoginForm,
    RegisterForm,
    AddPortfolioForm,
    generate_edit_portfolio_form,
    AddOrderForm,
    generate_edit_order_form,
    AddAlertForm,
    AddMarketWatchInstrument,
)


@pytest.mark.parametrize("data, errors, status", request.user_login_data)
def test_user_login_form(
    client, _db, load_environment_data, data: dict, errors: dict, status: bool
):
    """Test login form."""

    form = LoginForm(**data)
    assert form.validate() is status
    for key, error in errors.items():
        assert form.errors.get(key) == error


@pytest.mark.parametrize("data, errors, status", request.user_register_data)
def test_user_register_form(
    client, _db, load_environment_data, data: dict, errors: dict, status: bool
):
    """Test register form."""

    form = RegisterForm(**data)
    assert form.validate() is status
    for key, error in errors.items():
        assert form.errors.get(key) == error


@pytest.mark.parametrize("data, errors, status", request.add_portfolio_data)
def test_add_portfolio_form(
    client, _db, load_environment_data, login, data: dict, errors: dict, status: bool
):
    """Test add portfolio form."""

    form = AddPortfolioForm(**data)
    assert form.validate() is status
    for key, error in errors.items():
        assert form.errors.get(key) == error


@pytest.mark.parametrize("data, errors, status", request.edit_portfolio_data)
def test_edit_portfolio_form(
    client, _db, load_environment_data, login, data: dict, errors: dict, status: bool
):
    """Test edit portfolio form."""

    edit_form = generate_edit_portfolio_form(Portfolio.find_by_id(1))
    form: FlaskForm = edit_form(**data)
    assert form.validate() is status
    for key, error in errors.items():
        assert form.errors.get(key) == error


@pytest.mark.parametrize("data, errors, status", request.add_order_data)
def test_add_order_form(
    client, _db, load_environment_data, login, data: dict, errors: dict, status: bool
):
    """Test add order form."""

    form = AddOrderForm(**data)
    assert form.validate() is status
    for key, error in errors.items():
        assert form.errors.get(key) == error


@pytest.mark.parametrize("data, errors, status", request.edit_order_data)
def test_edit_order_form(
    client, _db, load_environment_data, login, data: dict, errors: dict, status: bool
):
    """Test edit order form."""

    edit_form = generate_edit_order_form(Order.find_by_id(1))
    form: FlaskForm = edit_form(**data)
    assert form.validate() is status
    for key, error in errors.items():
        assert form.errors.get(key) == error


@pytest.mark.parametrize("data, errors, status", request.add_alert_data)
def test_add_alert_form(
    client, _db, load_environment_data, login, data: dict, errors: dict, status: bool
):
    """Test add alert form."""

    form = AddAlertForm(**data)
    assert form.validate() is status
    for key, error in errors.items():
        assert form.errors.get(key) == error


@pytest.mark.parametrize("data, errors, status", request.add_market_watch_data)
def test_market_watch_instrument_form(
    client, _db, load_environment_data, login, data: dict, errors: dict, status: bool
):
    """Test add market watch instrument form."""

    form = AddMarketWatchInstrument(**data)
    assert form.validate() is status
    for key, error in errors.items():
        assert form.errors.get(key) == error
