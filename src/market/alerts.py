"""Market Movements"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from src.market.security.utils.value import SingleValue


@dataclass
class MarketSignal(ABC):
    """Base class for price direction."""

    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the signal."""

    @abstractmethod
    def check(self, target: float) -> bool:
        """Check if market movement is achieved."""


@dataclass
class ReturnType(ABC):
    """Base class for return types."""

    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the return type."""

    @abstractmethod
    def rule(self, target: float) -> bool:
        """Return calculation rule."""


@dataclass
class HoldingPeriodReturn(ReturnType):
    """Real return."""

    average_cost: SingleValue
    start_date: date
    real_return: bool = False


@dataclass
class Up(MarketSignal):
    """Up Movement."""

    value: float

    def __repr__(self) -> str:
        return f"Upper than: {self.value}"

    def check(self, target):
        return target > self.value


@dataclass
class Down(MarketSignal):
    """Down Movement."""

    value: float

    def __repr__(self) -> str:
        return f"Lower than: {self.value}"

    def check(self, target):
        return target < self.value


@dataclass
class Between(MarketSignal):
    """Between Movement."""

    low: float
    high: float

    def __repr__(self) -> str:
        return f"Between: {self.low} and {self.high}"

    def check(self, target):
        return self.low < target < self.high
