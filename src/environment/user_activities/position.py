import datetime

from src.extensions import db
from src.environment.user_activities.order import Order
from src.environment.user_activities.base import BaseModel

import yfinance as yf
import pandas as pd


class Position(BaseModel):
    __tablename__ = "positions"

    id = db.Column(db.Integer(), primary_key=True)
    symbol = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    security_type = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    portfolio_id = db.Column(
        db.Integer(),
        db.ForeignKey("portfolios.id"),
    )

    orders = db.relationship("Order", backref="position", cascade="all, delete-orphan")

    attr_dict = {
        "name": "Name",
        "security_type": "Security Type",
        "currency": "Currency",
        "market_cap": "Market Cap",
    }

    def __repr__(self):
        return "<Position {}.>".format(self.symbol)

    @property
    def open_quantity(self):
        quantity = 0
        for order in self.orders:
            quantity += order.adjusted_quantity
        return quantity

    @property
    def market_cap(self, quote: pd.DataFrame = None) -> float:
        if quote is None:
            md_provider = yf.Ticker(self.symbol)
        return float(round(md_provider.history(period="1d")["Close"], 2))

    @property
    def open(self) -> bool:
        return True if self.quantity != 0 else False

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).first()
