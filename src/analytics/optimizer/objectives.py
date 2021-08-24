"""Objective functions"""

# pylint: disable=invalid-name

from abc import ABC, abstractmethod
from dataclasses import dataclass

from numpy import ndarray
import cvxpy as cv


@dataclass
class ObjectiveFunc(ABC):
    """Base class for objective functions."""

    @abstractmethod
    def function(self, risk: cv.Variable, l, ret: cv.Expression):
        """Objective function."""

    @abstractmethod
    def constraint(self, mu: ndarray, w: cv.Variable, rf: float, k: cv.Variable):
        """Objective function."""


@dataclass
class MaxRiskAdjRet(ObjectiveFunc):
    """Maximize risk adjusted return."""

    def function(self, risk: cv.Variable, l, ret: cv.Expression):
        return cv.Minimize(risk * 1000)

    def constraint(self, mu: ndarray, w: cv.Variable, rf: float, k: cv.Variable):
        return [mu @ w - rf * k == 1]


@dataclass
class MinRisk(ObjectiveFunc):
    """Minimize risk."""

    def function(self, risk: cv.Variable, l, ret: cv.Expression):
        return cv.Minimize(risk * 1000)

    def constraint(self, mu: ndarray, w: cv.Variable, rf: float, k: cv.Variable):
        return []


@dataclass
class MaxUtility(ObjectiveFunc):
    """Maximize utility."""

    factor: float = 2  # Risk aversion factor.

    def function(self, risk: cv.Variable, l, ret: cv.Expression):
        return cv.Maximize(ret - l * risk)

    def constraint(self, mu: ndarray, w: cv.Variable, rf: float, k: cv.Variable):
        return []


@dataclass
class MaxReturn(ObjectiveFunc):
    """Maximize return."""

    def function(self, risk: cv.Variable, l, ret: cv.Expression):
        return cv.Maximize(ret)

    def constraint(self, mu: ndarray, w: cv.Variable, rf: float, k: cv.Variable):
        return []
