"""Form validation"""
# pylint: disable=too-few-public-methods

from datetime import datetime

from flask_login import current_user
from wtforms.validators import ValidationError

from src.environment import User, Portfolio
from src.market import Symbol, Info


class Ticker:
    """Validate ticker symbol."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        symbol = Symbol(field.data)
        if not symbol.is_valid:
            if not self.message:
                self.message = "Invalid Ticker!"
            raise ValidationError(self.message)


class Location:
    """Validate order market by currency."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        symbol = Symbol(field.data)
        if symbol.is_valid and symbol.get_info(Info.currency) not in ["USD", "CAD"]:
            if not self.message:
                self.message = "Only US and Canadian securities are supported!"
            raise ValidationError(self.message)


class PortfolioString:
    """Validate portfolio string."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data not in [port.name for port in current_user.portfolios]:
            if not self.message:
                self.message = "Portfolio name is not valid!"
            raise ValidationError(self.message)


class TradingDay:
    """Validate if the given date is trading day."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data < datetime.now():
            symbol = Symbol(form.symbol.data)
            if symbol.is_valid and not symbol.is_trading_day(field.data.date()):
                if not self.message:
                    self.message = "Given date is not a trading day."
                raise ValidationError(self.message)


class Underlying:
    """Validate if the underlying is a valid portfolio or a symbol."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        instrument_alerts = [
            "Price Signal",
            "Daily Return Signal",
            "Limit Return Signal",
        ]
        if form.signal.data in instrument_alerts:
            ticker_validator = Ticker()
            ticker_validator(form, field)
        else:
            portfolio_validator = PortfolioString()
            portfolio_validator(form, field)


class DateIfRequired:
    """Validate date if required."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if form.signal.data == "Limit Return Signal" and field.data is None:
            if not self.message:
                self.message = "Date must be provided when signal is limit signal!"
            raise ValidationError(self.message)


class FutureDate:
    """Validate execution date."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data and field.data > datetime.now():
            if not self.message:
                self.message = "Can not accept a future date!"
            raise ValidationError(self.message)


class PositiveFloat:
    """Validate if input is a positive float."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if field.data < 0:
            if not self.message:
                self.message = "Input should be 0 or more!"
            raise ValidationError(self.message)


class PortfolioName:
    """Validation for portfolio name duplication."""

    def __init__(self, exclude=None, message=None):
        self.message = message
        self.exclude = exclude

    def __call__(self, form, field):
        portfolio_names = [
            port.name
            for port in Portfolio.query.filter_by(
                user=current_user, name=field.data
            ).all()
        ]
        if self.exclude in portfolio_names:
            portfolio_names.remove(self.exclude)
        if portfolio_names:
            if not self.message:
                self.message = "Portfolio with the name {} already exists.".format(
                    field.data
                )
            raise ValidationError(self.message)


class UserNotExists:
    """Validate if email already exists in the db."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        if User.find_by_email(field.data):
            if not self.message:
                self.message = f"User with {field.data} email address already exists."
            raise ValidationError(self.message)


class Authorized:
    """Validate given password is correct."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        user = User.find_by_email(form.email.data)
        if not self.authenticate(user, field.data):
            if not self.message:
                self.message = (
                    "Invalid email, password or account has not been confirmed yet."
                )
            raise ValidationError(self.message)

    @staticmethod
    def authenticate(user: User, password: str) -> bool:
        """Authenticate the user."""
        return bool(user and user.check_password(password) and user.confirmed)


class WatchlistTicker:
    """Validate given ticket does not exist in the database."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        user: User = current_user
        if [
            instrument
            for instrument in user.watch_list
            if instrument.instrument.symbol == Symbol(field.data)
        ]:
            if not self.message:
                self.message = f"Given ticker: {field.data} already exists."
            raise ValidationError(self.message)
