from trading_calendars import get_calendar
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
from datetime import datetime, timedelta, timezone
from wtforms.fields.html5 import DateTimeField
from wtforms.validators import DataRequired, Length, ValidationError, Optional
from src.environment.order import Order
from src.environment.utils.types import *
from src.market_data.provider import YFinance


order_side_choices = [
    (OrderSideType.Buy, OrderSideType.Buy),
    (OrderSideType.Sell, OrderSideType.Sell),
]

date_time_format = "%Y-%m-%d"


class Ticker(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        md_provider = YFinance([field.data])
        if not md_provider.is_valid:
            if not self.message:
                self.message = "Invalid Ticker!"
            raise ValidationError(self.message)


class Location(object):
    def __init__(self, message=None):
        self.message = message

    def __call__(self, form, field):
        md_provider = YFinance([field.data])
        info = md_provider.info()
        if info[field.data]["currency"] not in [Currency.USD, Currency.CAD]:
            if not self.message:
                self.message = "Only US and Canadian securities are supported!"
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

    symbol = StringField(u"Ticker", [DataRequired(), Ticker(), Location()])
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

        date = self.exec_datetime.data.replace(tzinfo=timezone.utc)

        md_provider = YFinance([self.symbol.data])
        info = md_provider.info()
        currency = info[self.symbol.data]["currency"]
        calender = get_calendar(CurrencyExchangeMap[currency])

        if not calender.is_session(date):
            self.exec_datetime.errors.append("Selected date is holiday.")
            return False

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
            u"Order Date",
            [Optional(), FutureDate()],
            default=order.exec_time,
            format=date_time_format,
        )
        price = FloatField(u"Quote", [Optional()], default=order.exec_price)

        def validate(self):
            check_validate = super(EditOrderForm, self).validate()

            if not check_validate:
                return False

            date = self.exec_datetime.data.replace(tzinfo=timezone.utc)

            md_provider = YFinance([self.symbol.data])
            info = md_provider.info()
            currency = info[self.symbol.data]["currency"]
            calender = get_calendar(CurrencyExchangeMap[currency])

            if not calender.is_session(date):
                self.exec_datetime.errors.append("Selected date is holiday.")
                return False

            return True

    return EditOrderForm()
