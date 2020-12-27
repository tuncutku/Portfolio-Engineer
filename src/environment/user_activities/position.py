from pydantic.dataclasses import dataclass
from typing import List

from src.db import DB_Position

@dataclass
class Position:
    symbol: str
    quantity: int
    state: str
    portfolio_id: int
    position_id: int = None

    @classmethod
    def find_all(cls, portfolio_id: int, position_filter: List[str] = ["Open", "Closed"]) -> List["Position"]:
        position_list = DB_Position.get_positions(portfolio_id)
        return [cls(*position) for position in position_list if position[2] in position_filter]

    @classmethod
    def find_by_symbol(cls, symbol: str, portfolio_id: int) -> "Position":
        position = DB_Position.get_position(symbol, portfolio_id)
        return cls(*position)

    @staticmethod
    def add_position(symbol: str, quantity: int, port_id: int) -> None:
        DB_Position.add_position(symbol, quantity, "Open", port_id)

    def update_position(self, quantity: int, state: str = "Open") -> None:
        DB_Position.update_position(quantity, state, self.position_id)

    @classmethod
    def generate_by_orders(cls, orders: list):
        pass

    def add():
        pass
