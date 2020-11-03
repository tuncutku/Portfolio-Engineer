from dataclasses import dataclass

@dataclass
class Portfolio:
    portfolio_name: str
    user: str
    questrade_name: str
    balance: float
    positions: list

    _id: int = None
