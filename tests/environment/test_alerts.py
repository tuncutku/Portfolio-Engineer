"""Test alert objects"""
# pylint: disable=unused-argument

from pandas import Series

from src.environment import Portfolio, DailyReport, MarketAlert, alerts
from src.market import SingleValue
from src.market.ref_data import gspc, usd_ccy
from tests.test_data import environment as env


def test_daily_alert_object(client, _db, load_environment_data):
    """Test saved order object."""

    portfolio = Portfolio.find_by_id(1)
    alert = portfolio.daily_report
    assert alert == DailyReport.find_by_id(1)
    assert alert.id == 1
    assert alert.active is False


def test_daily_report_alert(client, _db, load_environment_data):
    """Unit test for daily alert methods."""

    daily_alert = DailyReport.find_by_id(1)
    assert daily_alert.condition()
    assert daily_alert.email_template == "email/daily_report.html"
    assert daily_alert.recipients[0] == env.user_1_raw["email"]

    content = daily_alert.generate_email_content()

    assert content["Main"]["Portfolio name"] == "portfolio_1"
    assert content["Main"]["Portfolio type"] == "Margin"
    assert content["Main"]["Benchmark"] == gspc
    assert content["Main"]["Reporting currency"] == usd_ccy
    assert isinstance(content["Main"]["Creation date"], str)
    assert isinstance(content["Main"]["Current market value"], SingleValue)


def test_price_alert(client, _db, load_environment_data):
    """Unit test for daily alert methods."""

    price_alert = MarketAlert.find_by_id(1)

    assert price_alert.condition()
    assert price_alert.email_template == "email/market_alert.html"
    assert price_alert.recipients[0] == env.user_1_raw["email"]

    content = price_alert.generate_email_content()
    assert str(content["symbol"]) == "AAPL"
    # assert str(content["alert_type"]) == "AAPL"
    # assert str(content["condition"]) == "AAPL"
    # assert str(content["target"]) == "AAPL"
    assert isinstance(content["current_value"], SingleValue)
    assert isinstance(content["triggered_time"], str)

    price_alert.deactivate()
    assert not price_alert.active