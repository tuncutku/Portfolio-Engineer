from flask_wtf import FlaskForm as Form
from wtforms import (
    StringField,
    BooleanField,
    SelectField,
    DecimalField,
    IntegerField,
    TimeField,
    DateField,
    DateTimeField,
    FloatField,
)
from datetime import datetime, timedelta
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from src.environment.user_activities.order import Order, OrderSideType

import yfinance as yf


order_side_choices = [
    (OrderSideType.Buy, OrderSideType.Buy),
    (OrderSideType.Sell, OrderSideType.Sell),
]

date_time_format = "%Y-%m-%d %H:%M"
date_format = "%Y-%m-%d"


def valide_price_and_date(ticker, price, date: datetime):

    validation = True
    now = datetime.now()
    security = yf.Ticker(ticker)

    # Case where date and price are not given.
    if not price and not date:
        try:
            price = float(round(security.history(period="1d")["Close"], 2))
            date = now
        except:
            validation = False

    # Case where only price is given.
    elif price and not date:
        date = now

    # Case where only the date is given.
    elif not price and date:
        # TODO: make this hourly and move to a new tahoo class.
        if date.date() == now.date():
            try:
                df = security.history(period="1m", interval="1m")
                price = float(df["Close"].round(2))
                date = now
            except:
                validation = False
        else:
            next_day = date + timedelta(days=1)
            try:
                df = security.history(
                    start=date.strftime(date_format), end=next_day.strftime(date_format)
                )
                price = float(df["Close"].round(2).values)
                if not price:
                    raise ValueError
            except (OverflowError, ValueError, TypeError):
                validation = False
    return validation, price, date


class Ticker(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        security = yf.Ticker(field.data)
        try:
            security.info
        except KeyError:
            if not self.message:
                self.message = "Invalid Ticker!"
            raise ValidationError(self.message)


class FutureDate(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        now = datetime.now()
        if field.data > now:
            if not self.message:
                self.message = "Can not accept a future date!"
            raise ValidationError(self.message)


class PositiveFloat(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        now = datetime.now()
        if field.data < 0:
            if not self.message:
                self.message = "Fee should be 0 or more!"
            raise ValidationError(self.message)


class AddOrderForm(Form):

    symbol = StringField(u"Ticker", [DataRequired(), Ticker()])
    quantity = IntegerField(u"Order Quantity", [DataRequired()])
    side = SelectField(
        u"Order Side", default=OrderSideType.Buy, choices=order_side_choices
    )
    fee = FloatField(u"Order Fee", [Optional(), PositiveFloat()], default=0)
    exec_datetime = DateTimeField(
        u"Order Date",
        [Optional(), FutureDate()],
        render_kw={"placeholder": datetime.now().strftime(date_time_format)},
        format=date_time_format,
    )
    price = FloatField(u"Quote", [Optional()])

    def validate(self):
        check_validate = super(AddOrderForm, self).validate()

        if not check_validate:
            return False

        valid, price, date = valide_price_and_date(
            self.symbol.data, self.price.data, self.exec_datetime.data
        )

        if not valid:
            self.price.errors.append(
                "Couldn't find a valid quote, please insert a quote for the underlying."
            )
            return False

        self.price.data = price
        self.exec_datetime.data = date

        return True


def generate_edit_order_form(order: Order):
    class EditOrderForm(Form):
        symbol = StringField(
            u"Ticker", [DataRequired(), Ticker()], default=order.symbol
        )
        quantity = IntegerField(
            u"Order Quantity", [DataRequired()], default=order.quantity
        )
        side = SelectField(
            u"Order Side", default=order.side, choices=order_side_choices
        )
        fee = FloatField(u"Order Fee", [Optional(), PositiveFloat()], default=order.fee)
        exec_datetime = DateTimeField(
            u"Order Date", [Optional(), FutureDate()], default=order.exec_time
        )
        price = FloatField(u"Quote", [Optional()], default=order.avg_exec_price)

        def validate(self):
            check_validate = super(EditOrderForm, self).validate()

            if not check_validate:
                return False

            valid, price, date = valide_price_and_date(
                self.symbol.data, self.price.data, self.exec_datetime.data
            )

            if not valid:
                self.price.errors.append(
                    "Couldn't find a valid quote, please insert a quote for the underlying."
                )
                return False

            self.price.data = price
            self.exec_datetime.data = date

            return True

    return EditOrderForm()
