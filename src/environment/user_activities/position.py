from pydantic.dataclasses import dataclass
from typing import List

from src.db import database

@dataclass
class Position:
    symbol: str
    quantity: int
    portfolio_id: str
    position_id: int = None

    @property
    def status(self) -> str:
        return "active" if self.quantity != 0 else "closed"

    @classmethod
    def find_all(cls):
        pass

    @classmethod
    def find_by_id(cls):
        pass

    @classmethod
    def generate_by_orders(cls, orders: list):
        pass

    def add():
        pass
