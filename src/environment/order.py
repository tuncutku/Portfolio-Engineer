"""Order"""
# pylint: disable=no-member, too-many-arguments, cyclic-import

from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime
from pandas import Series

from src.extensions import db
from src.environment.base import BaseModel
from src.market import SingleValue
from src.market.types import OrderSideType

if TYPE_CHECKING:
    from src.environment.position import Position


class Order(BaseModel):
    """Form an order class."""

    __tablename__ = "orders"

    quantity: float = db.Column(db.Integer(), nullable=False)
    direction: str = db.Column(db.String(255), nullable=False)
    cost: SingleValue = db.Column(db.PickleType(), nullable=False)
    time: datetime = db.Column(db.DateTime, nullable=False)

    position: Position = db.relationship("Position", back_populates="orders")
    position_id = db.Column(db.Integer(), db.ForeignKey("positions.id"))

    def __init__(
        self,
        quantity: float,
        direction: str,
        cost: SingleValue,
        time: datetime = datetime.now(),
    ) -> None:

        self.quantity = quantity
        self.direction = direction
        self.cost = cost
        self.time = time

    def __repr__(self) -> str:
        return f"<Order quantity: {self.quantity}, direction: {self.direction}.>"

    @property
    def adjusted_quantity(self) -> float:
        """Quantity of the order adjusted by the direction."""
        return (
            self.quantity
            if self.direction == OrderSideType.Buy
            else (-1) * self.quantity
        )

    @property
    def cost_df(self) -> Series:
        """Purchase price and fee of the order."""
        return Series([self.cost.value], index=[self.time], name="Cost")

    @property
    def quantity_df(self) -> Series:
        """Quantity of the order."""
        return Series([self.adjusted_quantity], index=[self.time], name="Quantity")

    def edit(
        self,
        quantity: float,
        direction: str,
        cost: SingleValue,
        time: datetime,
    ) -> None:
        """Edit an existing order."""

        self.quantity = quantity
        self.direction = direction
        self.cost = cost
        self.time = time
        db.session.commit()
