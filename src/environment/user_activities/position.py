from pydantic.dataclasses import dataclass
from typing import Union
import pandas as pd

security_type_map = {}


@dataclass
class Position:

    name: Union[str, None]
    symbol: Union[str, None]
    security_type: Union[str, None]
    currency: Union[str, None]

    def orders(self, orders):
        pass

    @property
    def quantity(self):
        total_position_quantity = sum(
            [
                order.filledQuantity
                if order.side == "Buy"
                else order.filledQuantity * -1
                for order in orders
            ]
        )
        pass

    @property
    def open(self) -> bool:
        pass

    def generate_trades(self, orders):
        pass

    @classmethod
    def from_dict(
        cls,
        symbol: str,
        shortName: str,
        quoteType: str,
        currency: str,
    ):
        return cls(shortName, symbol, quoteType, currency)

    @staticmethod
    def position_attributes_map():
        return {
            "Symbol": "symbol",
            "Name": "name",
            "Type": "security_type",
            "Currency": "currency",
        }
