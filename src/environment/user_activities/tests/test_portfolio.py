import pytest
from pydantic import ValidationError

from src.environment.user_activities.portfolio import Portfolio
from src.environment.user_activities.tests.raw_objects.portfolios import portofolio_dict


def test_create_user():
    """Unit test to check portfolio attributes."""

    for port_test in portofolio_dict["correct"]:
        port = Portfolio(
            port_test["name"],
            port_test["source"],
            port_test["status"],
            port_test["portfolio_type"],
            port_test["email"],
            port_test["questrade_id"],
            port_test["portfolio_id"],
        )
        for attribute, output in port_test.items():
            assert getattr(port, attribute) == output

    for port_test in portofolio_dict["wrong"]:
        with pytest.raises(ValidationError):
            port = Portfolio(
                port_test["name"],
                port_test["source"],
                port_test["status"],
                port_test["portfolio_type"],
                port_test["email"],
                port_test["questrade_id"],
                port_test["portfolio_id"],
            )