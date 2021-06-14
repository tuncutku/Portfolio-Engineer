"""Order forms"""
# pylint: disable=arguments-differ, invalid-name, super-with-arguments


from datetime import date

from flask_wtf import FlaskForm as Form
from wtforms import StringField, SelectField, DateTimeField, FloatField
from wtforms.validators import DataRequired, Optional

from src.market import get_business_day
from src.forms.validators import DateIfRequired, FutureDate, Underlying

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
    """Form a limit return signal alert form object."""

    signal = SelectField(u"Signal", default="Price Signal", choices=signal_choices)
    underlying = StringField(u"Underlying", [DataRequired(), Underlying()])
    operator = SelectField(u"Operator", default="Up", choices=operator_choices)
    target = FloatField(u"Target", [DataRequired()])
    start_date = DateTimeField(
        u"Limit Date",
        [DateIfRequired(), Optional(), FutureDate()],
        default=get_business_day(date.today()),
        format=date_time_format,
    )