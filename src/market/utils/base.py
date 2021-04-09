"""Base for securities."""
# pylint: disable=no-name-in-module
from abc import abstractmethod, ABC
from pydantic.dataclasses import dataclass
from pandas import DataFrame
from src.market.currency import Currency


@dataclass
class Security(ABC):
    """Base class for securities."""

    @property
    @abstractmethod
    def currency(self) -> Currency:
        """Currency of underlying security."""

    @property
    @abstractmethod
    def current_value(self) -> float:
        """Current value of underlying security."""

    @abstractmethod
    def index(self, start, end) -> DataFrame:
        """Index of the underlying security."""
