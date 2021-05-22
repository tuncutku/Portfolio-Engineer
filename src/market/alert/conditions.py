"""Market Movements"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Condition(ABC):
    """Base class for value condition."""

    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the signal."""

    @abstractmethod
    def check(self, target: float) -> bool:
        """Check if market movement is achieved."""


@dataclass
class Up(Condition):
    """Up Movement."""

    value: float

    def __repr__(self) -> str:
        return f"upper than: {self.value}"

    def check(self, target):
        return target > self.value


@dataclass
class Down(Condition):
    """Down Movement."""

    value: float

    def __repr__(self) -> str:
        return f"lower than: {self.value}"

    def check(self, target):
        return target < self.value


@dataclass
class Between(Condition):
    """Between Movement."""

    low: float
    high: float

    def __repr__(self) -> str:
        return f"between: {self.low} and {self.high}"

    def check(self, target):
        return self.low < target < self.high
