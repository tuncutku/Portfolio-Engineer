import datetime
import pandas as pd
from functools import cached_property
from typing import List

from src.extensions import db
from src.environment.utils.base import BaseModel
from src.environment.order import Order
from src.market_data.provider import YFinance


class Position(BaseModel):
    __tablename__ = "positions"

    portfolio_id = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    symbol = db.Column(db.String(255), nullable=False)
    security_type = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)

    orders: List[Order] = db.relationship(
        "Order", backref="position", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return "<Position {}.>".format(self.symbol)

    @cached_property
    def underlying_instrument(self):
        pass

    @cached_property
    def current_market_cap(self, reporting_currency: str):
        pass

    @cached_property
    def historical_market_cap(self, reporting_currency: str):
        pass

    @classmethod
    def find_by_symbol(cls, symbol, portfolio):
        return cls.query.filter_by(symbol=symbol, portfolio=portfolio).first()

    @property
    def open_quantity(self):
        return sum([order.adjusted_quantity for order in self.orders])

    @property
    def market_cap(self, quote: float = None) -> float:
        if quote is None:
            md_provider = YFinance([self.symbol])
            raw_quotes = md_provider.get_current_quotes()
        return round(float(raw_quotes[self.symbol] * self.open_quantity), 2)

    @property
    def open(self) -> bool:
        return True if self.open_quantity != 0 else False

    def to_dict(self):

        order_list = [order.to_dict() for order in self.orders]
        order_list.sort(key=lambda x: x.get("exec_time"), reverse=True)

        return {
            "ID": self.id,
            "Symbol": self.symbol,
            "Name": self.name,
            "Security Type": self.security_type,
            "Currency": self.currency,
            "Market Cap": "{:,.2f}".format(self.market_cap),
            "Total Quantity": self.open_quantity,
            "Open": self.open,
            "Orders": order_list,
        }

    def orders_df(self):
        order_df_list = [order.to_df() for order in self.orders]
        order_df = pd.concat(order_df_list)
        order_df_sorted = order_df.sort_index()
        order_df_sorted["Quantity"] = order_df_sorted["Quantity"].cumsum()
        return order_df_sorted