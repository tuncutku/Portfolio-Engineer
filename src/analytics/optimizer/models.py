"""Models used for optimizer"""

# pylint: disable=invalid-name

from abc import ABC, abstractmethod
from dataclasses import dataclass

import numpy as np
from pandas import DataFrame, Series
from scipy import linalg as LA
from statsmodels.stats.correlation_tools import cov_nearest


@dataclass
class MeanMethod:
    """Mean methods."""

    hist = "hist"
    ewma1 = "ewma1"
    ewma2 = "ewma2"


@dataclass
class Model(ABC):
    """Base model."""

    returns: DataFrame
    sector_map: dict = None

    def __post_init__(self):
        columns = self.returns.columns.tolist()
        columns.sort()
        self.returns = self.returns[columns]

    @property
    def nav(self):
        """Net asset value of the retuns."""
        return self.returns.cumsum()

    @staticmethod
    def check_cov_matrix(cov: DataFrame, threshold=1e-8) -> bool:
        """Indicate if a matrix is positive (semi)definite."""
        cov_ = np.array(cov, ndmin=2)
        w, _ = LA.eigh(cov_, lower=True, check_finite=True)
        return np.all(w >= threshold)

    @staticmethod
    def fix_cov_matrix(cov: DataFrame, threshold=1e-8) -> bool:
        """Fix a covariance matrix to a positive definite matrix."""
        cols = cov.columns.tolist()
        cov_ = np.array(cov, ndmin=2)
        cov_ = cov_nearest(cov_, method="clipped", threshold=threshold)
        cov_ = np.array(cov_, ndmin=2)
        return DataFrame(cov_, index=cols, columns=cols)

    @property
    @abstractmethod
    def mu(self) -> Series:
        """Mean of the retuns."""

    @property
    @abstractmethod
    def sigma(self) -> DataFrame:
        """Covariance of the retuns."""


@dataclass
class MeanVarianceModel(Model):
    """
    Model that estimates of expected return vector and covariance
    matrix that depends on historical data.
    """

    method: str = MeanMethod.hist
    d: float = 0.94

    @property
    def mu(self) -> Series:
        """Calculate mean of the returns."""
        return self.returns.ewm(alpha=1 - self.d).mean().iloc[-1, :]

    @property
    def sigma(self) -> DataFrame:
        """Covariance matrix of the returns."""
        cov = self.returns.ewm(alpha=1 - self.d).cov()
        item = cov.iloc[-1, :].name[0]
        cov = cov.loc[(item, slice(None)), :]
        if not self.check_cov_matrix(cov):
            cov = self.fix_cov_matrix(cov, 1e-5)
        return cov


# @dataclass
# class BlackLittermanModel(Model):
#     """
#     Model that estimates of expected return vector and covariance
#     matrix based on the Black Litterman model.
#     """


# @dataclass
# class FactorRiskModel(Model):
#     """
#     Model that use estimates of expected return vector and covariance
#     matrix a Risk Factor model.
#     """


# @dataclass
# class BlackLittermanRiskFactorModel(Model):
#     """
#     Model that use estimates of expected return vector and covariance
#     matrix based on Black Litterman applied to a Risk Factor model.
#     """
