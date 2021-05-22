"""Market Signals"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from src.market.security.utils.base import Security
from src.market.alert.conditions import Condition

from src.analytics import holding_period_return


@dataclass
class Signal(ABC):
    """Base for signal."""

    security: Security
    condition: Condition

    @abstractmethod
    def __repr__(self) -> str:
        """Repr method."""

    @abstractmethod
    def __hash__(self) -> int:
        """Hash the underlying signal."""

    @property
    @abstractmethod
    def target(self) -> float:
        """Get target value."""

    def check(self) -> bool:
        """Check the signal condition."""
        return self.condition.check(self.target)


@dataclass
class Price(Signal):
    """Price signal."""

    def __repr__(self) -> str:
        return f"Price alert with the condition {self.condition}."

    @property
    def target(self) -> float:
        return self.security.value.value


@dataclass
class HoldingPeriodReturn(Signal):
    """Holding period return signal."""

    start_date: date = date.today()

    def __repr__(self) -> str:
        return f"Holding period return with the condition {self.condition}."

    @property
    def target(self) -> float:
        index = self.security.index(self.start_date)
        return holding_period_return(index, self.start_date)


@dataclass
class DailyReturn(Signal):
    """Holding period return signal."""


@dataclass
class TimeDependentReturn(Signal):
    """Holding period return signal."""

    def __repr__(self) -> str:
        return f"Time dependent return with the condition {self.condition}."

    @property
    def target(self) -> float:
        return super().target


@dataclass
class Volatility(Signal):
    """Volatility signal."""


@dataclass
class DailyVolume(Signal):
    """Volume signal."""


@dataclass
class MovingAverage(Signal):
    """Volume signal."""
