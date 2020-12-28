from pydantic.dataclasses import dataclass
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
    exec_time: str # ex: "2014-10-23T20:03:42.890000-04:00"
    strategyType: str # ex:"SingleLeg"
    portfolio_id: str
    fee: int = 0
    position_id: int = None
    order_id: int = None

    @classmethod
    def find_all(cls, position_id, date_range = None):
        order_list = DB_Order.get_orders(position_id)
        return [cls(*order) for order in order_list]






