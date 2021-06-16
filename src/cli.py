"""CLI"""

from datetime import datetime
import subprocess
import click
from pylint import epylint

from src.extensions import db

from src.environment import User, Portfolio, Position, Order
from src.market import SingleValue
from src.market.ref_data import aapl, buy


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

        user = User("tuncutku10@gmail.com", "1234")
        portfolio = Portfolio("My portfolio 1")
        position = Position(aapl)
        order = Order(
            10,
            buy,
            SingleValue(120, aapl.asset_currency),
            datetime(2020, 4, 1),
        )

        user.save_to_db()
        # alert = user.add_price_alert(aapl, Up(20))
        user.add_portfolio(portfolio)
        portfolio.add_position(position)
        position.add_order(order)

        user.confirm_user()
        portfolio.daily_report.activate()
        # alert.activate()

    @app.cli.command("init_db")
    def init_db():
        """Init database."""

        db.create_all()

    @app.cli.command("clear_db")
    def clear_db():

        db.drop_all()
