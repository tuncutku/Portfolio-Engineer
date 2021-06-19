"""Order forms"""
# pylint: disable=arguments-differ, invalid-name, super-with-arguments


from datetime import datetime

from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, DateTimeField, FloatField
from wtforms.validators import DataRequired

from src.market import get_business_day
from src.forms.validators import (
    DateIfRequired,
    FutureDate,
    Underlying,
    Ticker,
    Location,
    WatchlistTicker,
)

date_time_format = "%Y-%m-%d"
operator_choices = [
    ("Up", "Up"),
    ("Up or Equal", "Up or Equal"),
    ("Down", "Down"),
    ("Down or Equal", "Down or Equal"),
]

signal_choices = [
    ("Price Signal", "Price Signal"),
    ("Daily Return Signal", "Daily Return Signal"),
    ("Limit Return Signal", "Limit Return Signal"),
    ("Portfolio Value Signal", "Portfolio Value Signal"),
    ("Daily Portfolio Return Signal", "Daily Portfolio Return Signal"),
]


class AddAlertForm(Form):
    """Form a signal alert form object."""

    signal = SelectField(u"Signal", default="Price Signal", choices=signal_choices)
    underlying = StringField(u"Underlying", [DataRequired(), Underlying()])
    operator = SelectField(u"Operator", default="Up", choices=operator_choices)
    target = FloatField(u"Target", [DataRequired()])
    start_date = DateTimeField(
        u"Limit Date",
        [DateIfRequired(), FutureDate()],
        default=get_business_day(datetime.today()),
        format=date_time_format,
    )


class AddMarketWatchInstrument(Form):
    """Form an add marketwatch instrument form."""

    symbol = StringField(
        u"Ticker", [DataRequired(), Ticker(), Location(), WatchlistTicker()]
    )
