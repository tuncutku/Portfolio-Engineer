from pydantic.dataclasses import dataclass
import pandas as pd


@dataclass
class Position:

    name: str
    symbol: str
    security_type: str
    industry: str
    market: str
    currency: str

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
        longName: str,
        quoteType: str,
        industry: str,
        market: str,
        currency: str,
    ):
        return cls(symbol, "Custom", total_position_quantity, "Open", portfolio_id)
