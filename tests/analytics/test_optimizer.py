"""Test optimizer"""

# pylint: disable=invalid-name

from pandas import DataFrame

import riskfolio.Portfolio as pf

from src.analytics.optimizer.constraints import (
    AssetConstraint,
    Operator,
    SingleConstraintValue,
    ConstraintType,
)
from src.analytics.optimizer.optimizer import MeanRiskOptimizer
from src.analytics.optimizer.models import MeanVarianceModel
from src.market.types import SecurityType, Sector

from tests.analytics.raw_data import raw_portfolio

portfolio_info = DataFrame(
    {
        ConstraintType.asset: ["AAPL", "FB", "PBW"],
        ConstraintType.security: [
            SecurityType.equity,
            SecurityType.equity,
            SecurityType.etf,
        ],
        ConstraintType.sector: [
            Sector.consumer_discretionary,
            Sector.consumer_discretionary,
            Sector.energy,
        ],
    }
)

portfolio_returns = DataFrame(raw_portfolio)


def test_asset_constraint():
    """Test asset constriant."""

    raw_direct_constraints = (
        (SingleConstraintValue("AAPL"), Operator.smaller, 0.4),
        (SingleConstraintValue("FB"), Operator.smaller, 0.5),
        (SingleConstraintValue("PBW"), Operator.greater, 0.1),
        (
            SingleConstraintValue(SecurityType.equity, ConstraintType.security),
            Operator.smaller,
            0.1,
        ),
    )

    raw_relative_constraints = (
        (SingleConstraintValue("AAPL", relative_value="FB"), Operator.smaller, 0.4),
        (
            SingleConstraintValue(
                Sector.consumer_discretionary, ConstraintType.sector, Sector.energy
            ),
            Operator.greater,
            1.2,
        ),
    )

    constraint = AssetConstraint(portfolio_info)

    for constr_value, operator, target in raw_direct_constraints:
        constraint.add_direct_constraint(constr_value, operator, target)

    for constr_value, operator, target in raw_relative_constraints:
        constraint.add_relative_constraint(constr_value, operator, target)


def test_models():
    """Test models."""

    rm_list = [
        "MV",
        "MAD",
        "MSV",
        "CVaR",
        "WR",
        "FLPM",
        "SLPM",
        "MDD",
        "ADD",
        "CDaR",
        "UCI",
        "EVaR",
        "EDaR",
    ]
    for rm in rm_list:

        model = MeanVarianceModel(portfolio_returns)
        optimizer = MeanRiskOptimizer(model, rm)
        result = optimizer.solve()

        w = get_benchmark_weights(portfolio_returns, rm, "Sharpe")
        assert all(w.round(4) == result.weights.round(4))


def get_benchmark_weights(returns, rm, obj):
    """Get benchmark weights."""

    port = pf.Portfolio(returns=returns)
    port.assets_stats(method_mu="ewma1", method_cov="ewma1", d=0.94)
    return port.optimization("Classic", rm=rm, obj=obj, rf=0, l=0, hist=True).values
