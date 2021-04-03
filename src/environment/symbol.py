import datetime
import pandas as pd

from src.extensions import db
from src.environment.utils.base import BaseModel
from src.market_data.provider import YFinance


class Symbol(BaseModel):
    __tablename__ = "symbols"

    symbol = db.Column(db.String(255), nullable=False)
    security_type = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)

    # Equity
    company = db.Column(db.String(255))

    # ETF
    holdings = db.Column(db.String(255))

    # Option
    strike = db.Column(db.Float())
    notional = db.Column(db.Float())
    expiry = db.Column(db.DateTime)

    def __repr__(self):
        return "<Position {}.>".format(self.symbol)