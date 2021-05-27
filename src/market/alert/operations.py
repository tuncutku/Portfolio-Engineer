"""Market Movements"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Operator(ABC):
    """Base class for operators."""

    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the signal."""

    @abstractmethod
    def check(self, target: float) -> bool:
        """Check if market movement is achieved."""


@dataclass
class Up(Operator):
    """Up operator."""

    value: float

    def __repr__(self) -> str:
        return f"upper than: {self.value}"

    def check(self, target):
        return target > self.value


@dataclass
class UpEqual(Operator):
    """Up or equal operator."""

    value: float

    def __repr__(self) -> str:
        return f"upper or equal than: {self.value}"

    def check(self, target):
        return target >= self.value


@dataclass
class Down(Operator):
    """Down operator."""

    value: float

    def __repr__(self) -> str:
        return f"lower than: {self.value}"

    def check(self, target):
        return target < self.value


@dataclass
class DownEqual(Operator):
    """Down or equal operator."""

    value: float

    def __repr__(self) -> str:
        return f"lower than: {self.value}"

    def check(self, target):
        return target <= self.value
