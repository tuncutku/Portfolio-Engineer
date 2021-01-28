import pytest
from pydantic import ValidationError

from src.environment.user_activities.order import Order
from src.environment.user_activities.tests.raw_objects.orders import order_dict


def test_create_order():
    """Unit test to check position attributes."""

    for order_test in order_dict["correct"]:
        order = Order(
            order_test["symbol"],
            order_test["source"],
            order_test["state"],
            order_test["filledQuantity"],
            order_test["side"],
            order_test["avg_exec_price"],
            order_test["exec_time"],
            order_test["strategyType"],
            order_test["portfolio_id"],
            order_test["fee"],
            order_test["position_id"],
            order_test["order_id"],
        )
        for attribute, output in order_test.items():
            assert getattr(order, attribute) == output

    for order_test in order_dict["wrong"]:
        with pytest.raises(ValidationError):
            Order(
                order_test["symbol"],
                order_test["source"],
                order_test["state"],
                order_test["filledQuantity"],
                order_test["side"],
                order_test["avg_exec_price"],
                order_test["exec_time"],
                order_test["strategyType"],
                order_test["portfolio_id"],
                order_test["fee"],
                order_test["position_id"],
                order_test["order_id"],
            )
