from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import List

from src.db import DB_Order

# TODO: Add leg property for multileg options
@dataclass
class Order:
    symbol: str
    source: str
    state: str # ex: "Canceled"
    filledQuantity: int
    side: str # ex: Buy
    avg_exec_price: float
    exec_time: datetime # ex: "2014-10-23T20:03:42.890000-04:00"
    strategyType: str # ex:"SingleLeg"
    portfolio_id: int
    fee: int = 0
    position_id: int = None
    order_id: int = None

    @classmethod
    def find_all(cls, position_id, date_range = None):
        order_list = DB_Order.get_orders(position_id)
        return [cls(*order) for order in order_list]
    
    @staticmethod
    def add_order(
        symbol: str,
        source: str,
        state: str,
        filledQuantity: int,
        side: str,
        avg_exec_price: float,
        exec_time: datetime,
        strategyType: str,
        portfolio_id: int,
        fee: float = 0.0,
        position_id: int = None,
    ) -> None:
        DB_Order.add_order(
            symbol,
            source,
            state,
            filledQuantity,
            side,
            avg_exec_price,
            exec_time,
            strategyType,
            fee,
            portfolio_id,
            position_id,
        )






