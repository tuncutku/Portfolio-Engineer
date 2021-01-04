from pydantic.dataclasses import dataclass
from typing import List

from src.db import DB_Position

@dataclass
class Position:
    symbol: str
    source: str
    quantity: int
    state: str
    portfolio_id: int
    position_id: int = None

    @classmethod
    def find_all(cls, portfolio_id: int, position_filter: List[str] = ["Open", "Closed"]) -> List["Position"]:
        position_list = DB_Position.get_positions(portfolio_id)
        return [cls(*position) for position in position_list if position[3] in position_filter]

    @classmethod
    def find_by_symbol(cls, symbol: str, portfolio_id: int) -> "Position":
        position = DB_Position.get_position(symbol, portfolio_id)
        return cls(*position)

    @classmethod
    def generate_by_orders(cls, orders: list, symbol: str, portfolio_id:int):
        total_position_quantity = sum(
            [order.filledQuantity if order.side == "Buy" else order.filledQuantity * -1 for order in orders]
        )
        return cls(symbol, "Custom", total_position_quantity, "Open", portfolio_id)

    def add_position(self) -> None:
        DB_Position.add_position(self.symbol, self.source, self.quantity, self.state, self.portfolio_id)

    def update_position(self, quantity: int, state: str = "Open") -> None:
        DB_Position.update_position(quantity, state, self.position_id)

    def delete_position(self) -> None:
        DB_Position.delete_position(self.position_id)
