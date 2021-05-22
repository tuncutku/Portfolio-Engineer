"""Market Signals"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from src.market.security.utils.base import Security
from src.market.alert.conditions import Condition


@dataclass
class Signal(ABC):
    """Base for signal."""

    security: Security
    condition: Condition

    @abstractmethod
    def __repr__(self) -> str:
        """Repr method."""

    @property
    @abstractmethod
    def target(self) -> float:
        """Get target value."""

    def check(self) -> bool:
        """Check the signal condition."""
        return self.condition.check(self.target)


class Price(Signal):
    """Price signal."""

    def __repr__(self) -> str:
        return "Price alert."

    @property
    def target(self) -> float:
        return self.security.value.value


class HoldingPeriodReturn(Signal):
    """Holding period return signal."""

    start_date: date

    def __repr__(self) -> str:
        return "Holding period return."

    @property
    def target(self) -> float:
        index = self.security.index(self.start_date)


class DailyReturn(Signal):
    """Holding period return signal."""


class PeakReturn(Signal):
    """Holding period return signal."""


class Volatility(Signal):
    """Volatility signal."""


class DailyVolume(Signal):
    """Volume signal."""


class MovingAverage(Signal):
    """Volume signal."""
