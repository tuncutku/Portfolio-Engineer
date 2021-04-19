# pylint: disable=no-member, too-many-arguments

from datetime import datetime
from pandas import DataFrame

from src.extensions import db
from src.environment.utils.base import BaseModel
from src.environment.utils.types import OrderSideType


class Order(BaseModel):
    """Form an order class."""

    __tablename__ = "orders"

    quantity: float = db.Column(db.Integer(), nullable=False)
    direction: str = db.Column(db.String(255), nullable=False)
    price: float = db.Column(db.Float(), nullable=False)
    time: datetime = db.Column(db.DateTime, nullable=False)
    fee: float = db.Column(db.Float(), default=0)

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

    def edit(
        self,
        quantity: float,
        direction: str,
        price: float,
        time: datetime,
        fee: float,
    ) -> None:
        """Edit an existing order."""

        self.quantity = quantity
        self.direction = direction
        self.price = price
        self.time = time
        self.fee = fee
        db.session.commit()

    def to_df(self) -> DataFrame:
        """Convert order to dataframe."""
        return DataFrame(
            data=[[self.adjusted_quantity, self.price, self.fee]],
            index=[self.time],
            columns=["Quantity", "Quote", "Fee"],
        )
