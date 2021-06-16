"""Order forms"""
# pylint: disable=arguments-differ, invalid-name, super-with-arguments


from datetime import datetime

from flask_wtf import FlaskForm as Form
from wtforms import (
    StringField,
    SelectField,
    IntegerField,
    DateTimeField,
    FloatField,
)
from wtforms.validators import DataRequired, Optional
from src.environment import Order
from src.market.ref_data import buy, sell
from src.forms.validators import Ticker, Location, FutureDate, PositiveFloat, TradingDay


direction_choices = [
    (buy, buy),
    (sell, sell),
]

date_time_format = "%Y-%m-%d"


class AddOrderForm(Form):
    """Form an order form object."""

    symbol = StringField(u"Ticker", [DataRequired(), Ticker(), Location()])
    quantity = IntegerField(u"Order Quantity", [DataRequired()])
    direction = SelectField(u"Direction", default=buy, choices=direction_choices)
    cost = FloatField(u"Cost", [Optional(), PositiveFloat()], default=0)
    exec_datetime = DateTimeField(
        u"Order Date",
        [DataRequired(), FutureDate(), TradingDay()],
        render_kw={"placeholder": datetime.now().strftime(date_time_format)},
        format=date_time_format,
    )


def generate_edit_order_form(order: Order) -> Form:
    """Create edit form object to edit an existing form."""

    class EditOrderForm(Form):
        """Form an order form object."""

        symbol = StringField(
            u"Ticker",
            [DataRequired(), Ticker()],
            default=order.position.security.symbol,
        )
        quantity = IntegerField(
            u"Order Quantity", [DataRequired()], default=order.quantity
        )
        direction = SelectField(
            u"Direction", default=order.direction, choices=direction_choices
        )
        cost = FloatField(
            u"Cost", [Optional(), PositiveFloat()], default=order.cost.value
        )
        exec_datetime = DateTimeField(
            u"Order Date",
            [DataRequired(), FutureDate(), TradingDay()],
            default=order.time,
            format=date_time_format,
        )

    return EditOrderForm()
