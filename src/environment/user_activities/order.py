from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import List

from src.db import DB_Order

# TODO: Add leg property for multileg options
# TODO: Add currency
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
    def find_all(cls, position_id, date_range = None) -> List["Order"]:
        order_list = DB_Order.get_orders(position_id = position_id)
        return [cls(*order) for order in order_list]

    @classmethod
    def find_all_by_symbol(cls, portfolio_id: int, symbol: str) -> List["Order"]:
        order_list = DB_Order.get_orders_by_symbol(portfolio_id = portfolio_id, symbol = symbol)
        return [cls(*order) for order in order_list]
    
    @classmethod
    def find_by_id(cls, order_id) -> "Order":
        order = DB_Order.get_order(order_id)
        return cls(*order)

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

    def update_order(
        self,
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
        DB_Order.update_order(
            symbol,
            source,
            state,
            filledQuantity,
            side,
            avg_exec_price,
            exec_time,
            strategyType,
            portfolio_id,
            fee,
            position_id,
            self.order_id
        )
    
    def insert_position_id(self, position_id: int) -> None:
        DB_Order.update_position_id(self.order_id, position_id)

    def delete_order(self) -> None:
        DB_Order.delete_order(self.order_id)



