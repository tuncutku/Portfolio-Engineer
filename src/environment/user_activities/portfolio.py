import datetime

from sqlalchemy_serializer import SerializerMixin
from src import db_1


class PortfolioTag:
    primary = "Primary"
    regular = "Regular"


class Currency:
    CAD = "CAD"
    USD = "USD"


class PortfolioType:
    tfsa = "TFSA"
    rrsp = "RRSP"
    margin = "Margin"
    cash = "Cash"
    custom = "Custom"


class PortfolioStatus:
    active = "Active"
    inactive = "Inactive"


class PortfolioSource:
    questrade = "Questrade"
    custom = "Custom"


class Portfolio(db_1.Model, SerializerMixin):
    __tablename__ = "portfolios"

    id = db_1.Column(db_1.Integer(), primary_key=True)
    name = db_1.Column(db_1.String(255), nullable=False)
    user_id = db_1.Column(db_1.Integer(), db_1.ForeignKey("users.id"))
    portfolio_type = db_1.Column(db_1.String(255), nullable=False)
    reporting_currency = db_1.Column(db_1.String(3), nullable=False)

    # Questrade attributes
    questrade_id = db_1.Column(db_1.Integer())
    source = db_1.Column(db_1.String(255), default=PortfolioSource.custom)

    # Default attributes
    portfolio_tag = db_1.Column(db_1.String(255), default=PortfolioTag.regular)
    date = db_1.Column(db_1.DateTime(), default=datetime.datetime.now)

    orders = db_1.relationship(
        "Order", backref="portfolios", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        name: str,
        user_id: int,
        portfolio_type: str = PortfolioType.custom,
        reporting_currency: str = Currency.CAD,
    ):
        self.name = name
        self.user_id = user_id
        self.portfolio_type = portfolio_type
        self.reporting_currency = reporting_currency

    def __repr__(self):
        return "<Portfolio {}.>".format(self.name)

    def set_questrade_attributes(questrade_id):
        self.source = PortfolioSource.questrade
        self.questrade_id = questrade_id
