"""Position"""
# pylint: disable=no-member, not-an-iterable, too-many-arguments, cyclic-import

from __future__ import annotations

from datetime import date
from typing import List, TYPE_CHECKING, Union
from pandas import concat, Series, bdate_range

from src.extensions import db
from src.environment.base import BaseModel
from src.environment.order import Order
from src.market import Instrument, Currency, SingleValue, IndexValue, Info

if TYPE_CHECKING:
    from src.environment.portfolio import Portfolio


class Position(BaseModel):
    """Form a position class."""

    __tablename__ = "positions"

    security: Instrument = db.Column(db.PickleType(), nullable=False)

    portfolio_id: int = db.Column(db.Integer(), db.ForeignKey("portfolios.id"))
    portfolio: Portfolio = db.relationship("Portfolio", back_populates="positions")
    orders: List[Order] = db.relationship(
        "Order", back_populates="position", cascade="all, delete-orphan"
    )

    def __init__(self, security: Instrument) -> None:
        self.security = security

    def __repr__(self) -> str:
        return f"<Position {self.security.symbol.symbol}.>"

    @property
    def is_open(self) -> bool:
        """True if current open quantity is different than 0."""
        return bool(self.open_quantity)

    @property
    def quantity(self) -> Series:
        """Quantity of the position."""
        return concat([order.quantity_df for order in self.orders]).sort_index()

    def cumulative_quantity_index(
        self, start: date, end: date = date.today()
    ) -> Series:
        """Cumulative quantity of the position."""
        raw_brange = bdate_range(self.quantity.index.min().date(), date.today())
        raw_index = self.quantity.cumsum().reindex(raw_brange, method="ffill")
        index = raw_index.reindex(bdate_range(start, end))
        return index.rename(self.security.symbol.symbol).fillna(0)

    @property
    def open_quantity(self) -> Union[float, int]:
        """Open quantity of the position."""
        return sum(self.quantity)

    @property
    def cost(self) -> Series:
        """Cost of the position including purchase price and fee."""
        return concat([order.cost_df for order in self.orders]).sort_index()

    def current_value(
        self, currency: Currency = None, request: str = Info.price
    ) -> SingleValue:
        """Current value of the security."""
        value = self.security.value(request)
        if currency:
            value = value.to(currency)
        return value * self.open_quantity

    def security_historical_value(
        self, start: date, end: date = date.today(), currency: Currency = None
    ) -> IndexValue:
        """Get security historical value, updated with transaction costs."""
        index = self.security.index(start, end)
        index.replace(self.cost)
        if currency:
            index = index.to(currency)
        return index

    def historical_value(
        self, start: date, end: date = date.today(), currency: Currency = None
    ) -> IndexValue:
        """Get value index of the underlying position."""
        security_value = self.security_historical_value(start, end, currency)
        quantity = self.cumulative_quantity_index(start, end)
        return security_value * quantity

    def add_order(self, order: Order, save: bool = True) -> Order:
        """Add new order."""
        order.position = self
        if save:
            order.save_to_db()
        return order
