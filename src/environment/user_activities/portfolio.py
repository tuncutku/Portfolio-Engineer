import datetime
from typing import List

from src.environment.user_activities.base import BaseModel
from src.environment.user_activities.position import Position

from sqlalchemy_serializer import SerializerMixin
from src.extensions import db

import yfinance as yf


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


class Portfolio(BaseModel):
    __tablename__ = "portfolios"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    name = db.Column(db.String(255), nullable=False)
    portfolio_type = db.Column(db.String(255), nullable=False)
    reporting_currency = db.Column(db.String(3), nullable=False)

    # Questrade attributes
    # questrade_id = db.Column(db.Integer())
    # source = db.Column(db.String(255), default=PortfolioSource.custom)

    # Default attributes
    portfolio_tag = db.Column(db.String(255), default=PortfolioTag.regular)
    date = db.Column(db.DateTime(), default=datetime.datetime.now)

    positions = db.relationship(
        "Position", backref="portfolio", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return "<Portfolio {}.>".format(self.name)

    # def set_questrade_attributes(questrade_id):
    #     self.source = PortfolioSource.questrade
    #     self.questrade_id = questrade_id

    @property
    def total_mkt_value(self):
        md_provider = yf.Ticker("EURUSD=X")
        fx_rate = float(round(md_provider.history(period="1d")["Close"], 2))
        value = 0
        for pos in self.positions:
            pos_mkt_cap = (
                pos.market_cap
                if pos.currency == self.reporting_currency
                else pos.market_cap * fx_rate
            )
            value += pos_mkt_cap
        return round(value, 2)

    @classmethod
    def find_by_id(cls, _id: int):
        return cls.query.get(_id)

    def edit(self, name, currency, port_type):
        self.name = name
        self.reporting_currency = currency
        self.portfolio_type = port_type
        db.session.commit()
