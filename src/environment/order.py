"""Order"""
# pylint: disable=no-member, too-many-arguments

from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime
from pandas import Series

from src.extensions import db
from src.environment.utils.base import BaseModel
from src.environment.utils.types import OrderSideType

if TYPE_CHECKING:
    from src.environment.position import Position


class Order(BaseModel):
    """Form an order class."""

    __tablename__ = "orders"

    quantity: float = db.Column(db.Integer(), nullable=False)
    direction: str = db.Column(db.String(255), nullable=False)
    cost: float = db.Column(db.Float(), nullable=False)
    time: datetime = db.Column(db.DateTime, nullable=False)

    position_id = db.Column(db.Integer(), db.ForeignKey("positions.id"))

    def __repr__(self):
        return f"<Order quantity: {self.quantity}, direction: {self.direction}.>"

    @property
    def adjusted_quantity(self):
        """Quantity of the order adjusted by the direction."""
        return (
            self.quantity
            if self.direction == OrderSideType.Buy
            else (-1) * self.quantity
        )

    @property
    def cost_df(self) -> Series:
        """Purchase price and fee of the order."""
        return Series([self.cost], index=[self.time], name="Cost")

    @property
    def quantity_df(self) -> Series:
        """Quantity of the order."""
        return Series([self.adjusted_quantity], index=[self.time], name="Quantity")

    def edit(
        self,
        quantity: float,
        direction: str,
        cost: float,
        time: datetime,
    ) -> None:
        """Edit an existing order."""

        self.quantity = quantity
        self.direction = direction
        self.cost = cost
        self.time = time
        db.session.commit()
