"""Market Signals"""

# pylint: disable=line-too-long

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from math import log
from typing import TYPE_CHECKING, Union

from src.market.symbol import Info
from src.market.basic import Currency
from src.market.security.utils.base import Instrument
from src.market.signal.operators import Operator, Up, UpEqual, Down, DownEqual

# from src.market.types import Period

if TYPE_CHECKING:
    from src.environment import Portfolio


@dataclass
class Signal(ABC):
    """Base for signal."""

    underlying: Union[Instrument, Portfolio]
    operator: Operator
    target: float
    creation_date: date = field(init=False, default=date.today())
    active: bool = field(init=False, default=True)

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

    def apply_operator(self) -> bool:
        """Check the signal condition."""
        return self.operator.check(self.target, self.value)

    def activate(self) -> None:
        """Activate signal."""
        self.active = True

    def deactivate(self) -> None:
        """Activate signal."""
        self.active = False


@dataclass
class PriceSignal(Signal):
    """Price signal."""

    def __repr__(self) -> str:
        return f"Signal triggered when current price is {self.operator} than {self.target}."

    @property
    def value(self) -> float:
        return round(self.underlying.value.value, 5)


@dataclass
class DailyReturnSignal(Signal):
    """Price signal."""

    def __repr__(self) -> str:
        target_pct = "{0:.2f}%".format(self.target * 100)
        return (
            f"Signal triggered when daily return is {self.operator} than {target_pct}."
        )

    @property
    def value(self) -> float:
        current_price = self.underlying.value.value
        open_price = self.underlying.symbol.get_info(Info.market_open)
        return round(log(current_price / open_price), 5)


EXTREMA_MAP = {Up: min, UpEqual: min, Down: max, DownEqual: max}


@dataclass
class LimitReturnSignal(Signal):
    """Price signal."""

    start_date: date = date.today()

    def __repr__(self) -> str:
        target_pct = "{0:.2f}%".format(self.target * 100)
        return f"Signal triggered when the return calculated by max or min price from the starting date is {self.operator} than {target_pct}."

    @property
    def value(self) -> float:
        if self.start_date == date.today():
            value = 0
        else:
            current_price = self.underlying.value.value
            index = self.underlying.index(self.start_date)
            extrema = EXTREMA_MAP[type(self.operator)]
            value = round(log(current_price / extrema(index)), 5)
        return value


@dataclass
class DailyPortfolioReturnSignal(Signal):
    """Daily portfolio return signal."""

    def __repr__(self) -> str:
        target_pct = "{0:.2f}%".format(self.target * 100)
        return f"Signal triggered when portfolio daily return is {self.operator} than {target_pct}."

    @property
    def value(self) -> float:
        return self.underlying.current_value()


@dataclass
class PortfolioValueSignal(Signal):
    """Portfolio value signal."""

    currency: Currency = None

    def __repr__(self) -> str:
        target_pct = "{0:.2f}%".format(self.target * 100)
        return f"Signal triggered when current portfolio value is {self.operator} than {target_pct}."

    @property
    def value(self) -> float:
        return self.underlying.current_value(self.currency)


# @dataclass
# class MovingAverageSignal(Signal):
#     """Volume signal."""


# @dataclass
# class VolumeSignal(Signal):
#     """Volume signal."""
