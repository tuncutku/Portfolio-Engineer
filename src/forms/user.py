"""User forms"""
# pylint: disable=arguments-differ, invalid-name, super-with-arguments

from flask_wtf import FlaskForm as Form
from wtforms import PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from src.forms.validators import UserNotExists, Authorized


class RegisterForm(Form):
    """Register form."""

    email = EmailField("Email address", [DataRequired(), Email(), UserNotExists()])
    password = PasswordField("Password", [DataRequired(), Length(min=4)])
    confirm = PasswordField("Confirm Password", [DataRequired(), EqualTo("password")])


class LoginForm(Form):
    """Login form."""

    email = EmailField(u"Email address", [DataRequired()])
    password = PasswordField(u"Password", [DataRequired(), Authorized()])
