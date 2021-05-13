"""Position"""
# pylint: disable=no-member, not-an-iterable, too-many-arguments, cyclic-import

from datetime import datetime, date
from typing import List
from pandas import concat, Series

from src.extensions import db
from src.environment.base import BaseModel
from src.environment.order import Order
from src.market import Security, Currency, SingleValue, IndexValue


class Position(BaseModel):
    """Form a position class."""

    __tablename__ = "positions"

    security: Security = db.Column(db.PickleType(), nullable=False)

    portfolio_id: int = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    orders: List[Order] = db.relationship(
        "Order", backref="position", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Position {self.security.symbol.symbol}.>"

    @property
    def is_open(self) -> bool:
        """True if current open quantity is different than 0."""
        return bool(self.quantity.sum())

    @property
    def quantity(self) -> Series:
        """Quantity of the position."""
        return concat([order.quantity_df for order in self.orders]).sort_index()

    @property
    def cumulative_quantity(self) -> Series:
        """Cumulative quantity of the position."""
        date_index = self.security.index(self.quantity.index.min().date()).index.index
        return self.quantity.cumsum().reindex(date_index).fillna(method="ffill")

    @property
    def cost(self) -> Series:
        """Cost of the position including purchase price and fee."""
        return concat([order.cost_df for order in self.orders]).sort_index()

    def current_value(self, currency: Currency = None) -> SingleValue:
        """Current value of the security."""
        new_value = (
            self.security.value.to(currency) if currency else self.security.value
        )
        return new_value * self.quantity.sum()

    def historical_value(
        self, currency: Currency, start: date, end: date = date.today()
    ) -> IndexValue:
        """Get value index of the underlying position."""
        security_index = self.security.index(start, end)
        security_index.replace(self.cost)
        new_index = security_index.to(currency)
        return new_index * self.cumulative_quantity

    def add_order(
        self, quantity: float, direction: str, cost: float, time: datetime
    ) -> Order:
        """Add new order."""
        order = Order(
            quantity=quantity,
            direction=direction,
            cost=cost,
            time=time,
            position=self,
        )
        order.save_to_db()
        return order
