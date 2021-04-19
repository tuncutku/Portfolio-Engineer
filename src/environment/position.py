# pylint: disable=no-member, not-an-iterable, too-many-arguments

from datetime import datetime
from typing import List
import pandas as pd

from src.extensions import db
from src.environment.utils.base import BaseModel
from src.environment.order import Order
from src.market import Observable


class Position(BaseModel):
    """Form a position class."""

    __tablename__ = "positions"

    security: Observable = db.Column(db.PickleType(), nullable=False)

    portfolio_id: int = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    orders: List[Order] = db.relationship(
        "Order", backref="position", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Position {self.security}.>"

    @property
    def open_quantity(self):
        """Current open quantity of the position."""
        return sum([order.adjusted_quantity for order in self.orders])

    @property
    def orders_df(self) -> pd.DataFrame:
        """Get orders as dataframe."""
        return pd.concat([order.to_df() for order in self.orders], sort=True)

    def current_value(self, reporting_currency: str = None):
        """Current value of the security."""
        value = self.security.current_value
        # if reporting_currency and self.security.asset_currency != reporting_currency:
        #     pass

    # def historical_value(self, reporting_currency: str):
    #     pass

    def add_order(
        self, quantity: float, direction: str, price: float, time: datetime, fee: float
    ) -> Order:
        """Add new order."""
        order = Order(
            quantity=quantity,
            direction=direction,
            price=price,
            time=time,
            fee=fee,
            position=self,
        )
        order.save_to_db()
        return order
