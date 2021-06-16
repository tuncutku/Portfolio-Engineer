"""Form validation"""
# pylint: disable=too-few-public-methods

from datetime import datetime

from flask_login import current_user
from wtforms.validators import ValidationError

from src.environment import Portfolio
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
        if symbol.get_info(Info.currency) not in ["USD", "CAD"]:
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
        symbol = Symbol(form.symbol.data)
        if not symbol.is_trading_day(field.data.date()):
            if not self.message:
                self.message = "Given date is not a trading day."


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
        if form.signal.data == "Limit Return Signal" and field is None:
            if not self.message:
                self.message = "Date must be provided when signal is limit signal!"
            raise ValidationError(self.message)


class FutureDate:
    """Validate execution date."""

    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        now = datetime.now()
        if field.data > now:
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
                self.message = "Fee should be 0 or more!"
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
                self.message = u"Portfolio with the name {} already exists.".format(
                    field.data
                )
            raise ValidationError(self.message)
