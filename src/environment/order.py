import pandas as pd
from datetime import datetime
from typing import List

from src.extensions import db
from src.environment.utils.base import BaseModel
from src.environment.utils.types import *


class Order(BaseModel):
    __tablename__ = "orders"

    position_id = db.Column(db.Integer(), db.ForeignKey("positions.id"))
    symbol = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    side = db.Column(db.String(255), nullable=False)
    avg_exec_price = db.Column(db.Float(), nullable=False)
    exec_time = db.Column(db.DateTime, nullable=False)
    fee = db.Column(db.Float(), nullable=False)
    # strategyType: str  # ex:"SingleLeg"
    # fee: int = 0

    def __repr__(self):
        return "<Order {}.>".format(self.symbol)

    @property
    def adjusted_quantity(self):
        return self.quantity if self.side == OrderSideType.Buy else (-1) * self.quantity

    def to_dict(self):
        return {
            "ID": self.id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "side": self.side,
            "avg_exec_price": self.avg_exec_price,
            "exec_time": self.exec_time.strftime("%y-%m-%d %a %H:%M"),
            "fee": self.fee,
        }

    def edit(self, symbol, quantity, side, avg_exec_price, exec_time, fee) -> None:
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.avg_exec_price = avg_exec_price
        self.exec_time = exec_time
        self.fee = fee
        db.session.commit()

    def to_df(self):
        return pd.DataFrame(
            data=[[self.adjusted_quantity, self.avg_exec_price, self.fee]],
            index=[self.exec_time],
            columns=["Quantity", "Quote", "Fee"],
        )
