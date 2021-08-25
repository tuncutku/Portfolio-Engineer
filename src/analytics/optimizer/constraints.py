"""Constraint"""

# pylint: disable=invalid-name, too-many-instance-attributes

from dataclasses import dataclass
from enum import Enum
from typing import List

from numpy import zeros
from pandas import DataFrame, Series, concat


class Operator(Enum):
    """Operator used in constraint construction."""

    greater = 1
    smaller = -1

    def __mul__(self, other: float) -> float:
        return self.value * other

    def __rmul__(self, other) -> float:
        return self * other


@dataclass
class ConstraintType:
    """Costraint types."""

    asset = "Asset"
    security = "Security"
    sector = "Sector"


@dataclass
class ConstraintBase:
    """Constraint base class."""


@dataclass
class SingleConstraintValue:
    """Single Constraint type and value."""

    value: str
    type: str = ConstraintType.asset
    relative_value: str = None


@dataclass
class AssetConstraint(ConstraintBase):
    """Single asset constraint."""

    asset_info: DataFrame = None

    def __post_init__(self):
        self._validate_inputs()
        self.A = DataFrame(columns=self.assets)
        self.B = Series(dtype=float)

    def _validate_inputs(self) -> None:
        """Validate inputs."""

    @property
    def assets(self) -> List[str]:
        """Asset list."""
        return self.asset_info[ConstraintType.asset].tolist()

    @property
    def empty_row(self) -> DataFrame:
        """Get base constraint."""
        n = len(self.assets)
        return DataFrame(zeros((1, n)), columns=self.assets)

    def add_direct_constraint(
        self,
        constaint_value: SingleConstraintValue,
        operator: Operator,
        target_value: float,
    ):
        """Add new direct constraint."""

        row = self.empty_row
        assets = self._get_assets(constaint_value.type, constaint_value.value)
        for asset in assets:
            row[asset] = 1 * operator
        self._extend_new_row(row, operator * target_value)

    def add_relative_constraint(
        self,
        constaint_value: SingleConstraintValue,
        operator: Operator,
        target_value: float,
    ):
        """Add new relative constraint."""

        row = self.empty_row
        assets = self._get_assets(constaint_value.type, constaint_value.value)
        target_assets = self._get_assets(
            constaint_value.type, constaint_value.relative_value
        )
        for asset in assets:
            row[asset] = 1 * operator
        for asset in target_assets:
            row[asset] = target_value * operator * -1
        self._extend_new_row(row, 0)

    def _extend_new_row(self, a: DataFrame, b: float):
        """Add new A and B values to constraints."""

        self.A = concat([self.A, a])
        self.B = self.B.append(Series(b))

    def _get_assets(self, _type: str, _value: str) -> List[str]:
        """Filter assets from asset information."""

        filtered_df = self.asset_info.loc[self.asset_info[_type] == _value]
        return filtered_df[ConstraintType.asset].to_list()


@dataclass
class LimitConstraint(ConstraintBase):
    """Limit constraints."""

    lowerret: float = None
    upperdev: float = None
    uppermad: float = None
    uppersdev: float = None
    upperflpm: float = None
    upperslpm: float = None
    upperCVaR: float = None
    upperEVaR: float = None
    upperwr: float = None
    uppermdd: float = None
    upperadd: float = None
    upperCDaR: float = None
    upperEDaR: float = None
    upperuci: float = None
