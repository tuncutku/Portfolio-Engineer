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
    def check(self, target: float, value: float) -> bool:
        """Check if market movement is achieved."""


@dataclass
class Up(Operator):
    """Up operator."""

    def __repr__(self) -> str:
        return "upper"

    def check(self, target: float, value: float):
        return value > target


@dataclass
class UpEqual(Operator):
    """Up or equal operator."""

    def __repr__(self) -> str:
        return "upper or equal"

    def check(self, target: float, value: float):
        return value >= target


@dataclass
class Down(Operator):
    """Down operator."""

    def __repr__(self) -> str:
        return "lower"

    def check(self, target: float, value: float):
        return value < target


@dataclass
class DownEqual(Operator):
    """Down or equal operator."""

    def __repr__(self) -> str:
        return "lower or equal"

    def check(self, target: float, value: float):
        return value <= target
