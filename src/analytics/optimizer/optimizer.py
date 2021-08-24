"""Optimizer"""

# pylint: disable=invalid-name, too-many-instance-attributes, broad-except, too-many-branches, too-many-statements, too-many-locals

from dataclasses import dataclass
from functools import wraps
from typing import List

from numpy import ones, array, sqrt, log
from pandas import Series
import cvxpy as cv
from scipy.linalg import sqrtm

from src.analytics.optimizer.models import Model
from src.analytics.optimizer.constraints import AssetConstraint, LimitConstraint
from src.analytics.optimizer.objectives import ObjectiveFunc, MaxRiskAdjRet


@dataclass(frozen=True)
class OptimalResult:
    """Optimal result of the problem."""

    value: float = None
    weights: Series = None
    errors: str = None

    def __bool__(self):
        return bool(self.errors)


@dataclass
class PortfolioSettings:
    """Portfolio settings."""

    rf: float = 0
    sht: bool = False
    uppersht = 0.2
    upperlng = 1
    alpha: float = 0.05
    budget: float = 1
    l: float = 2
    sht: bool = False
    bench: Series = None
    allowTE: bool = None
    TE: bool = None


@dataclass
class Optimizer:
    """Optimizer base."""

    @classmethod
    def catch_error(cls, func) -> OptimalResult:
        """Decorator for catching optimization errors."""

        @wraps(func)
        def _call_wrapper(self, *args, **kwargs) -> OptimalResult:
            try:
                value, weights = func(self, *args, **kwargs)
                message = None
            except Exception as e:
                message = str(e)
                value = None
                weights = None
            return OptimalResult(value, weights, message)

        return _call_wrapper

    @property
    def solvers(self) -> List[str]:
        """Solver list."""
        return ["ECOS", "SCS", "OSQP", "CVXOPT"]

    @property
    def solver_params(self) -> dict:
        """Solver parameters."""
        return {
            "ECOS": {"max_iters": 500, "abstol": 1e-8},
            "SCS": {"max_iters": 2500, "eps": 1e-5},
            "OSQP": {"max_iter": 10000, "eps_abs": 1e-8},
            "CVXOPT": {"max_iters": 500, "abstol": 1e-8},
        }

    def list_constraints(self):
        """List all constraints."""


@dataclass
class MeanRiskOptimizer(Optimizer):
    """Optimizer."""

    model: Model
    risk: str = "MV"
    objective: ObjectiveFunc = MaxRiskAdjRet()
    limit_constraints: LimitConstraint = LimitConstraint()
    asset_constraints: AssetConstraint = None
    settings: PortfolioSettings = PortfolioSettings()

    def __post_init__(self):

        self.returns = array(self.model.returns, ndmin=2)
        # Mean and covariance matrices
        self.mu = self.model.mu.values
        self.sigma = self.model.sigma.values
        self.nav = self.model.nav.values
        # Variables
        self.n = len(self.returns)
        self.w = cv.Variable((len(self.mu), 1))
        self.k = cv.Variable((1, 1)) if isinstance(self.objective, MaxRiskAdjRet) else 1
        self.sharp_multiplier = 1000 if isinstance(self.objective, MaxRiskAdjRet) else 1
        self.ret = self.mu @ self.w

    def _add_asset_constraints(self):
        """Add weight constraint."""

        A = self.asset_constraints.A * 1000
        B = self.asset_constraints.B * 1000
        return [A @ self.w - B @ self.k >= 0]

    @property
    def mv_risk(self):
        """MV risk and variables."""

        g = cv.Variable(nonneg=True)
        G = sqrtm(self.sigma)
        risk1 = g
        devconstraints = [cv.SOC(g, G.T @ self.w)]
        return Risk(devconstraints, risk1)

    # @Optimizer.catch_error
    def solve(self) -> OptimalResult:
        """Solve the optimization problem."""

        # MV Model Variables
        g = cv.Variable(nonneg=True)
        G = sqrtm(self.sigma)
        risk1 = g
        devconstraints = [cv.SOC(g, G.T @ self.w)]

        # MAD Model Variables
        madmodel = False
        Y = cv.Variable((self.n, 1))
        u = ones((self.n, 1)) * self.mu
        a = self.returns - u
        risk2 = cv.sum(Y) / self.n
        madconstraints = [a @ self.w >= -Y, Y >= 0]

        # Semi Variance Model Variables
        risk3 = cv.norm(Y, "fro") / cv.sqrt(self.n - 1)

        # CVaR Model Variables
        VaR = cv.Variable((1, 1))
        X = self.returns @ self.w
        Z = cv.Variable((self.n, 1))
        risk4 = VaR + 1 / (self.settings.alpha * self.n) * cv.sum(Z)
        cvarconstraints = [Z >= 0, Z >= -X - VaR]

        # Worst Realization (Minimax) Model Variables
        M = cv.Variable((1, 1))
        risk5 = M
        wrconstraints = [-X <= M]

        # Lower Partial Moment Variables
        lpmmodel = False
        lpm = cv.Variable((self.n, 1))
        lpmconstraints = [lpm >= 0, lpm >= self.settings.rf * self.k - X]

        # First Lower Partial Moment (Omega) Model Variables
        risk6 = cv.sum(lpm) / self.n

        # Second Lower Partial Moment (Sortino) Model Variables
        risk7 = cv.norm(lpm, "fro") / cv.sqrt(self.n - 1)

        # Drawdown Model Variables
        drawdown = False
        X1 = self.k + self.nav @ self.w

        U = cv.Variable((self.nav.shape[0] + 1, 1))
        ddconstraints = [
            U[1:] * 1000 >= X1 * 1000,
            U[1:] * 1000 >= U[:-1] * 1000,
            U[1:] * 1000 >= self.k * 1000,
            U[0] * 1000 == self.k * 1000,
        ]

        # Maximum Drawdown Model Variables
        MDD = cv.Variable((1, 1))
        risk8 = MDD
        mddconstraints = [MDD >= U[1:] - X1]

        # Average Drawdown Model Variables
        risk9 = 1 / self.n * cv.sum(U[1:] - X1)

        # Conditional Drawdown Model Variables
        CDaR = cv.Variable((1, 1))
        Zd = cv.Variable((self.nav.shape[0], 1))
        risk10 = CDaR + 1 / (self.settings.alpha * self.n) * cv.sum(Zd)
        cdarconstraints = [
            Zd * 1000 >= U[1:] * 1000 - X1 * 1000 - CDaR * 1000,
            Zd * 1000 >= 0,
        ]

        # Ulcer Index Model Variables
        risk11 = cv.norm(U[1:] * 1000 - X1 * 1000, "fro") / sqrt(self.n)

        # Entropic Value at Risk Model Variables
        t1 = cv.Variable((1, 1))
        s1 = cv.Variable((1, 1), nonneg=True)
        ui = cv.Variable((self.n, 1))
        risk12 = t1 + s1 * log(1 / (self.settings.alpha * self.n))
        evarconstraints = [
            cv.sum(ui) * self.sharp_multiplier <= s1 * self.sharp_multiplier,
            cv.constraints.ExpCone(
                -X * self.sharp_multiplier - t1 * self.sharp_multiplier,
                ones((self.n, 1)) @ s1 * self.sharp_multiplier,
                ui * self.sharp_multiplier,
            ),
        ]

        # Entropic Drawdown at Risk Model Variables
        t2 = cv.Variable((1, 1))
        s2 = cv.Variable((1, 1), nonneg=True)
        uj = cv.Variable((self.n, 1))
        risk13 = t2 + s2 * log(1 / (self.settings.alpha * self.n))
        edarconstraints = [
            cv.sum(uj) * self.sharp_multiplier <= s2 * self.sharp_multiplier,
            cv.constraints.ExpCone(
                U[1:] * self.sharp_multiplier
                - X1 * self.sharp_multiplier
                - t2 * self.sharp_multiplier,
                ones((self.n, 1)) @ s2 * self.sharp_multiplier,
                uj * self.sharp_multiplier,
            ),
        ]

        # Problem Weight Constraints
        constraints = [
            cv.sum(self.w) == self.settings.budget * self.k,
            self.k * self.sharp_multiplier >= 0,
        ]
        if self.settings.sht is False:
            constraints += [
                self.w <= self.settings.upperlng * self.k,
                self.w * 1000 >= 0,
            ]

        elif self.settings.sht is True:
            constraints += [
                cv.sum(cv.pos(self.w)) * 1000 <= self.settings.upperlng * self.k * 1000,
                cv.sum(cv.neg(self.w)) * 1000 <= self.settings.uppersht * self.k * 1000,
            ]

        # Tracking error Constraints
        if self.settings.allowTE is True:
            bench = array(self.settings.bench, ndmin=2)
            TE_1 = cv.norm(self.returns @ self.w - bench @ self.k, "fro") / cv.sqrt(
                self.n - 1
            )
            constraints += [TE_1 * 1000 <= self.settings.TE * self.k * 1000]

        # Problem return Constraints
        if self.limit_constraints.lowerret is not None:
            constraints += [self.ret >= self.limit_constraints.lowerret * self.k]

        # Problem risk Constraints
        if self.limit_constraints.upperdev is not None:
            constraints += [risk1 <= self.limit_constraints.upperdev * self.k]
            constraints += self.mv_risk.constraints

        if self.limit_constraints.uppermad is not None:
            constraints += [risk2 <= self.limit_constraints.uppermad * self.k / 2]
            madmodel = True

        if self.limit_constraints.uppersdev is not None:
            constraints += [risk3 <= self.limit_constraints.uppersdev * self.k]
            madmodel = True

        if self.limit_constraints.upperCVaR is not None:
            constraints += [risk4 <= self.limit_constraints.upperCVaR * self.k]
            constraints += cvarconstraints

        if self.limit_constraints.upperwr is not None:
            constraints += [-X <= self.limit_constraints.upperwr * self.k]
            constraints += wrconstraints

        if self.limit_constraints.upperflpm is not None:
            constraints += [risk6 <= self.limit_constraints.upperflpm * self.k]
            lpmmodel = True

        if self.limit_constraints.upperslpm is not None:
            constraints += [risk7 <= self.limit_constraints.upperslpm * self.k]
            lpmmodel = True

        if self.limit_constraints.uppermdd is not None:
            constraints += [U[1:] - X1 <= self.limit_constraints.uppermdd * self.k]
            constraints += mddconstraints
            drawdown = True

        if self.limit_constraints.upperadd is not None:
            constraints += [risk9 <= self.limit_constraints.upperadd * self.k]
            drawdown = True

        if self.limit_constraints.upperCDaR is not None:
            constraints += [risk10 <= self.limit_constraints.upperCDaR * self.k]
            constraints += cdarconstraints
            drawdown = True

        if self.limit_constraints.upperuci is not None:
            constraints += [risk11 <= self.limit_constraints.upperuci * 1000 * self.k]
            drawdown = True

        if self.limit_constraints.upperEVaR is not None:
            constraints += [risk12 <= self.limit_constraints.upperEVaR * self.k]
            constraints += evarconstraints

        if self.limit_constraints.upperEDaR is not None:
            constraints += [risk13 <= self.limit_constraints.upperEDaR * self.k]
            constraints += edarconstraints

        if self.asset_constraints:
            constraints += self._add_asset_constraints()

        # Defining risk function
        if self.risk == "MV":
            risk = risk1
            if self.limit_constraints.upperdev is None:
                constraints += devconstraints
        elif self.risk == "MAD":
            risk = risk2
            madmodel = True
        elif self.risk == "MSV":
            risk = risk3
            madmodel = True
        elif self.risk == "CVaR":
            risk = risk4
            if self.limit_constraints.upperCVaR is None:
                constraints += cvarconstraints
        elif self.risk == "WR":
            risk = risk5
            if self.limit_constraints.upperwr is None:
                constraints += wrconstraints
        elif self.risk == "FLPM":
            risk = risk6
            lpmmodel = True
        elif self.risk == "SLPM":
            risk = risk7
            lpmmodel = True
        elif self.risk == "MDD":
            risk = risk8
            drawdown = True
            if self.limit_constraints.uppermdd is None:
                constraints += mddconstraints
        elif self.risk == "ADD":
            risk = risk9
            drawdown = True
        elif self.risk == "CDaR":
            risk = risk10
            drawdown = True
            if self.limit_constraints.upperCDaR is None:
                constraints += cdarconstraints
        elif self.risk == "UCI":
            risk = risk11
            drawdown = True
            l = self.settings.l / 1000
        elif self.risk == "EVaR":
            risk = risk12
            if self.limit_constraints.upperEVaR is None:
                constraints += evarconstraints
        elif self.risk == "EDaR":
            risk = risk13
            drawdown = True
            if self.limit_constraints.upperEDaR is None:
                constraints += edarconstraints

        if madmodel is True:
            constraints += madconstraints
        if lpmmodel is True:
            constraints += lpmconstraints
        if drawdown is True:
            constraints += ddconstraints

        # Get objective function and constraints.
        constraints += self.objective.constraint(
            self.mu, self.w, self.settings.rf, self.k
        )
        objective = self.objective.function(risk, l, self.ret)

        # for solver in self.solvers:
        problem = cv.Problem(objective, constraints)
        problem.solve(solver="ECOS")
        weights = self.w.value / self.k.value
        return OptimalResult(problem.value, weights)
