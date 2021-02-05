from flask_wtf import FlaskForm as Form
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.fields.html5 import EmailField
from wtforms.validators import (
    DataRequired,
    Length,
    ValidationError,
)
from flask_login import current_user

from src.environment.user_activities.portfolio import Portfolio, PortfolioType, Currency


port_type_choices = [
    (PortfolioType.custom, PortfolioType.custom),
    (PortfolioType.margin, PortfolioType.margin),
    (PortfolioType.tfsa, PortfolioType.tfsa),
    (PortfolioType.cash, PortfolioType.cash),
    (PortfolioType.rrsp, PortfolioType.rrsp),
]

currency_choices = [(Currency.CAD, Currency.CAD), (Currency.USD, Currency.USD)]


class PortfolioName(object):
    def __init__(self, exclude=None, message=None):
        self.message = message
        self.exclude = exclude

    def __call__(self, form, field):
        portfolio_names = [
            port.name
            for port in Portfolio.query.filter_by(
                user_id=current_user.id, name=field.data
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


class AddPortfolioForm(Form):
    port_name = StringField(
        u"Portfolio Name", [DataRequired(), Length(max=20), PortfolioName()]
    )
    port_type = SelectField(u"Portfolio Type", default=1, choices=port_type_choices)
    port_reporting_currency = SelectField(
        u"Reporting Currency", default=1, choices=currency_choices
    )


def generate_edit_portfolio_form(portfolio: Portfolio):
    """Function that generates an instance of EditPortfolioForm and sets default arguments."""

    portfolio_type_choice_index = [
        port_type for port_type, _ in port_type_choices
    ].index(portfolio.portfolio_type)

    portfolio_currency_index = [currency for currency, _ in currency_choices].index(
        portfolio.reporting_currency
    )

    class EditPortfolioForm(Form):
        port_name = StringField(
            u"Portfolio Name",
            [DataRequired(), Length(max=20), PortfolioName(exclude=portfolio.name)],
            default=portfolio.name,
        )
        port_type = SelectField(
            u"Portfolio Type",
            choices=port_type_choices,
            default=portfolio.portfolio_type,
        )
        port_reporting_currency = SelectField(
            u"Reporting Currency",
            choices=currency_choices,
            default=portfolio.reporting_currency,
        )

    return EditPortfolioForm()
