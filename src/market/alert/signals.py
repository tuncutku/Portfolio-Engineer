"""Market Signals"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from math import log

from src.market.security.utils.base import Security
from src.market.alert.operations import Operator
from src.market.types import Period


@dataclass
class Signal(ABC):
    """Base for signal."""

    security: Security
    condition: Operator
    creation_date: date = field(init=False, default=date.today())

    @abstractmethod
    def __repr__(self) -> str:
        """Repr method."""

    # @abstractmethod
    # def __hash__(self) -> int:
    #     """Hash the underlying signal."""

    @property
    @abstractmethod
    def target(self) -> float:
        """Get target value."""

    @abstractmethod
    def check_expiry(self) -> bool:
        """Check if the signal has expired."""

    def check_condition(self) -> bool:
        """Check the signal condition."""
        return self.condition.check(self.target)


@dataclass
class PriceSignal(Signal):
    """Price signal."""

    def __repr__(self) -> str:
        return f"Price alert with the condition {self.condition}."

    def check_expiry(self) -> bool:
        return False

    @property
    def target(self) -> float:
        return round(self.security.value.value, 5)


@dataclass
class BasicReturnSignal(Signal):
    """Price signal."""

    initial_price: float

    def __repr__(self) -> str:
        return f"Price alert with the condition {self.condition}."

    def check_expiry(self) -> bool:
        return False

    @property
    def target(self) -> float:
        current_price = self.security.value.value
        return round(log(current_price / self.initial_price), 5)


@dataclass
class PeriodReturnSignal(Signal):
    """Period return signal."""

    start_date: date = date.today()

    def __repr__(self) -> str:
        return f"Holding period return with the condition {self.condition}."

    @property
    def target(self) -> float:
        index = self.security.index(self.start_date)
        return holding_period_return(index, self.start_date)


@dataclass
class PeriodReturnSignal(Signal):
    """Holding period return signal."""

    period: Period = Period.day

    # daily, weekly, monthly, yearly


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
