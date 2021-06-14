"""Test portfolio endpoints"""
# pylint: disable=unused-argument

from datetime import date

import pytest

from src.environment import MarketAlert
from src.market.ref_data import aapl, up

from tests.test_data.request import successful_alerts
from tests.system.common import templete_used


# def test_portfolio_list(client, _db, load_environment_data, login, captured_templates):
#     """Test endpoint that lists portfolios."""

#     response = client.get("/portfolio/list")
#     assert response.status_code == 200

#     template_list = ["portfolio/list_portfolios.html"]
#     templete_used(template_list, captured_templates)


@pytest.mark.parametrize(
    "data", successful_alerts, ids=[alert["signal"] for alert in successful_alerts]
)
def test_add_alert(client, _db, load_environment_data, login, captured_templates, data):
    """Test endpoint that adds portfolio."""

    response = client.get("alert/add_alert")
    assert response.status_code == 200
    assert "Add new alert" in response.get_data(as_text=True)

    response = client.post("alert/add_alert", data=data, follow_redirects=True)
    assert response.status_code == 200

    alert = MarketAlert.find_by_id(2)
    assert alert.signal.underlying == aapl or alert.signal.underlying == "portfolio_1"
    assert alert.signal.operator == up
    assert alert.signal.target == data["target"]
    assert alert.signal.creation_date == date(2021, 6, 13)
    assert alert.signal.active is True

    template_list = ["alert/add_alert.html", "alert/list_alerts.html"]
    templete_used(template_list, captured_templates)

    assert not MarketAlert.find_by_id(3)
    response = client.post("alert/add_alert", data=data, follow_redirects=True)
    assert response.status_code == 200
    assert not MarketAlert.find_by_id(3)
