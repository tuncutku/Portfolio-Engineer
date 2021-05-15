"""Market Movements"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MarketSignal(ABC):
    """Base class for price direction."""

    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the signal."""

    @abstractmethod
    def check(self, price: float) -> bool:
        """Check if market movement is achieved."""


@dataclass
class Up(MarketSignal):
    """Up Movement."""

    value: float

    def __repr__(self) -> str:
        return f"Upper than: {self.value}"

    def check(self, price):
        return price > self.value


@dataclass
class Down(MarketSignal):
    """Down Movement."""

    value: float

    def __repr__(self) -> str:
        return f"Lower than: {self.value}"

    def check(self, price):
        return price < self.value


@dataclass
class Between(MarketSignal):
    """Between Movement."""

    low: float
    high: float

    def __repr__(self) -> str:
        return f"Between: {self.low} and {self.high}"

    def check(self, price):
        return self.low < price < self.high
