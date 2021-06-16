"""Test forms"""
# pylint: disable=unused-argument

from flask import request, current_app
from flask_wtf import FlaskForm
from src.forms import LoginForm, AddAlertForm


def post_data(data: dict, form_class) -> dict:
    """Post data to the app."""

    with current_app.test_request_context(method="POST", data=data):
        form: FlaskForm = form_class(request.form, meta={"csrf": False})
        result = form.validate_on_submit()
        errors = form.errors
    return {"Result": result, "Errors": errors}


def test_user_login_form(client, _db, load_environment_data):
    """Test login form."""

    form = post_data({"email": "tuncutku10@gmail.com"}, LoginForm)

    # new_form = LoginForm(email="tu", password="1")

    assert form


def test_add_alert_form(client, _db, load_environment_data):
    """Test add alert form."""

    data = {
        "signal": "Price Signal",
        "underlying": "AAPL",
        "operator": "Up",
        "target": "130",
    }

    form = post_data(data, AddAlertForm)
    assert form
