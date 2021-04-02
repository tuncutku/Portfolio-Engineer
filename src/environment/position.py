import datetime
import pandas as pd

from src.extensions import db
from src.environment.utils.base import BaseModel
from src.market_data.yahoo import YFinance


class Position(BaseModel):
    __tablename__ = "positions"

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

    portfolio_id = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    orders = db.relationship("Order", backref="position", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Position {}.>".format(self.symbol)

    @classmethod
    def find_by_symbol(cls, symbol, portfolio):
        return cls.query.filter_by(symbol=symbol, portfolio=portfolio).first()

    @property
    def open_quantity(self):
        quantity = 0
        for order in self.orders:
            quantity += order.adjusted_quantity
        return quantity

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