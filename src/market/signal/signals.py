"""Market Signals"""

# pylint: disable=line-too-long, trailing-whitespace

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from math import log
from typing import TYPE_CHECKING, Union

from flask_login import current_user

from src.market.symbol import Info
from src.market.basic import Currency
from src.market.security.utils.base import Instrument
from src.market.signal.operators import Operator, Up, UpEqual, Down, DownEqual

if TYPE_CHECKING:
    from src.environment import User


@dataclass
class Signal(ABC):
    """Base for signal."""

    underlying: Union[Instrument, str]
    operator: Operator
    target: float
    creation_date: date = field(init=False, default=date.today())

    @abstractmethod
    def __repr__(self) -> str:
        """Repr method."""

    @property
    @abstractmethod
    def signal_type(self) -> str:
        """Signal type."""

    @property
    @abstractmethod
    def value(self) -> float:
        """Get value to be compared with target."""

    def apply_operator(self) -> bool:
        """Check the signal condition."""
        return self.operator.check(self.target, self.value)


@dataclass
class PriceSignal(Signal):
    """Price signal."""

    def __repr__(self) -> str:
        return f"Signal triggered when current price is {self.operator} than {self.target}."

    @property
    def signal_type(self) -> str:
        return "Price signal"

    @property
    def value(self) -> float:
        return round(self.underlying.value(raw=True), 5)


@dataclass
class DailyReturnSignal(Signal):
    """Daily return signal."""

    def __repr__(self) -> str:
        target_pct = "{0:.2f}%".format(self.target * 100)
        return (
            f"Signal triggered when daily return is {self.operator} than {target_pct}."
        )

    @property
    def signal_type(self) -> str:
        return "Daily return signal"

    @property
    def value(self) -> float:
        current_price = self.underlying.value(raw=True)
        open_price = self.underlying.value(Info.market_open, raw=True)
        return round(log(current_price / open_price), 5)


EXTREMA_MAP = {Up: min, UpEqual: min, Down: max, DownEqual: max}


@dataclass
class LimitReturnSignal(Signal):
    """Limit return signal."""

    start_date: date = date.today()

    def __repr__(self) -> str:
        target_pct = "{0:.2f}%".format(self.target * 100)
        return f"Signal triggered when the return calculated by max or min price from the starting date is {self.operator} than {target_pct}."

    @property
    def signal_type(self) -> str:
        return "Limit return signal"

    @property
    def value(self) -> float:
        if self.start_date == date.today():
            value = 0
        else:
            current_price = self.underlying.value(raw=True)
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
    def signal_type(self) -> str:
        return "Daily portfolio return signal"

    @property
    def value(self) -> float:
        user: User = current_user
        portfolio = user.get_portfolio_by_name(self.underlying)
        current_value = portfolio.current_value()
        open_value = portfolio.current_value(request=Info.market_open)
        return round(log(current_value.value / open_value.value), 5)


@dataclass
class PortfolioValueSignal(Signal):
    """Portfolio value signal."""

    currency: Currency = None

    def __repr__(self) -> str:
        return f"Signal triggered when portfolio current value is {self.operator} than {self.target}."

    @property
    def signal_type(self) -> str:
        return "Portfolio value signal"

    @property
    def value(self) -> float:
        user: User = current_user
        portfolio = user.get_portfolio_by_name(self.underlying)
        return portfolio.current_value(self.currency).value
