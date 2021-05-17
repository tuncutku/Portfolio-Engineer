"""CLI"""

from datetime import datetime
import subprocess
import click
from pylint import epylint

from src.environment import User
from src.market import Equity, Symbol, Currency
from src.market.signal import Up
from src.market.types import PortfolioType, OrderSideType
from src.extensions import db


def register_cli(app):
    """Register command line interface."""

    @app.cli.command()
    @click.option(
        "--coverage/--no-coverage", default=False, help="Run tests under code coverage."
    )
    def test(coverage):

        if coverage:
            subprocess.call(
                [
                    "pytest",
                    "--cov=src",
                    "--cov-report",
                    "xml:cov.xml",
                    "--cov-config=.coveragerc",
                ]
            )
        else:
            subprocess.call(["pytest"])

    @app.cli.command("check_style")
    def check_style():

        epylint.py_run("src")

    @app.cli.command("create_user")
    def create_user():

        db.create_all()

        user = User(email="tuncutku10@gmail.com")
        user.save_to_db()
        user.set_password("1234")
        user.confirm_user()

        aapl = Equity(Currency("USD"), Symbol("AAPL"))

        alert = user.add_price_alert(aapl, Up(20))

        portfolio = user.add_portfolio("T", PortfolioType.custom, Currency("USD"), aapl)
        position = portfolio.add_position(aapl)
        position.add_order(10, OrderSideType.Buy, 120, datetime(2020, 4, 1))

        portfolio.daily_report.activate()
        alert.activate()

    @app.cli.command("clear_database")
    def clear_database():

        db.drop_all()
