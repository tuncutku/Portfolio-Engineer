import pytest
from pydantic import ValidationError

from src.environment.user_activities.position import Position
from src.environment.user_activities.tests.raw_objects.positions import position_dict


def test_create_position():
    """Unit test to check position attributes."""

    for pos_test in position_dict["correct"]:
        position = Position(
            pos_test["symbol"],
            pos_test["source"],
            pos_test["quantity"],
            pos_test["state"],
            pos_test["portfolio_id"],
            pos_test["position_id"],
        )
        for attribute, output in pos_test.items():
            assert getattr(position, attribute) == output

    for pos_test in position_dict["wrong"]:
        with pytest.raises(ValidationError):
            Position(
                pos_test["symbol"],
                pos_test["source"],
                pos_test["quantity"],
                pos_test["state"],
                pos_test["portfolio_id"],
                pos_test["position_id"],
            )
