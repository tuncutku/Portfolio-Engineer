"""Market Signals"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from math import log

from src.market.security.utils.base import Security
from src.market.alert.operators import Operator

# from src.market.types import Period


@dataclass
class Signal(ABC):
    """Base for signal."""

    security: Security
    operator: Operator
    target: float
    creation_date: date = field(init=False, default=date.today())

    @abstractmethod
    def __repr__(self) -> str:
        """Repr method."""

    # @abstractmethod
    # def __hash__(self) -> int:
    #     """Hash the underlying signal."""

    @property
    @abstractmethod
    def value(self) -> float:
        """Get value to be compared with target."""

    @abstractmethod
    def check_expiry(self) -> bool:
        """Check if the signal has expired."""

    def apply_operator(self) -> bool:
        """Check the signal condition."""
        return self.operator.check(self.target, self.value)


@dataclass
class PriceSignal(Signal):
    """Price signal."""

    def __repr__(self) -> str:
        return f"Signal triggered when current price is {self.operator} than {self.target}."

    def check_expiry(self) -> bool:
        return False

    @property
    def value(self) -> float:
        return round(self.security.value.value, 5)


@dataclass
class BasicReturnSignal(Signal):
    """Price signal."""

    initial_price: float

    def __repr__(self) -> str:
        target_pct = "{0:.2f}%".format(self.target * 100)
        return f"Signal triggered when return is {self.operator} than {target_pct}."

    def check_expiry(self) -> bool:
        return False

    @property
    def value(self) -> float:
        current_price = self.security.value.value
        return round(log(current_price / self.initial_price), 5)


# @dataclass
# class PeriodReturnSignal(Signal):
#     """Period return signal."""

#     start_date: date = date.today()
#     period: Period = Period.day
#     repeat: bool = True

#     def __repr__(self) -> str:
#         return f"Holding period return with the condition {self.operator}."

#     @property
#     def value(self) -> float:
#         index = self.security.index(self.start_date)
#         return holding_period_return(index, self.start_date)


# @dataclass
# class TimeDependentTargetReturn(Signal):
#     """Holding period return signal."""

#     def __repr__(self) -> str:
#         return f"Time dependent return with the condition {self.operator}."

#     @property
#     def value(self) -> float:
#         return super().target


# @dataclass
# class DurationBasedPriceSignal(Signal):
#     """Duran based high or low price signal."""

#     period: Period

#     def __repr__(self) -> str:
#         return f"Time dependent return with the condition {self.operator}."

#     @property
#     def value(self) -> float:
#         return super().target


# @dataclass
# class MovingAverageSignal(Signal):
#     """Volume signal."""


# @dataclass
# class VolumeSignal(Signal):
#     """Volume signal."""
