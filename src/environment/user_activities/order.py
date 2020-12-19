from pydantic.dataclasses import dataclass
from typing import List

from src.db import database
from src.services.questrade import Questrade

@dataclass
class Order:
    symbol: str
    state: str # ex: "Canceled",
    filledQuantity: int
    side: str # ex: Buy
	avgExecPrice: float,
	time: str # ex: "2014-10-23T20:03:42.890000-04:00",
	legs: str = None,
	strategyType: str # ex:"SingleLeg",
    fee: int = 0
    portfolio_id: str
    position_id: int = None
    order_id: int = None

    @classmethod
    def find_all(cls):
        pass

    @classmethod
    def find_by_id(cls):
        pass

    @classmethod
    def generate_by_orders(cls, orders: list):
        pass

    def add_position():
        pass





