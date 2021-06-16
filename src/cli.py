"""CLI"""

from datetime import datetime

from src.extensions import db

from src.environment import User, Portfolio, Position, Order, MarketAlert
from src.market import SingleValue
from src.market.ref_data import aapl, buy, up
from src.market.signal import PriceSignal


def register_cli(app):
    """Register command line interface."""

    @app.cli.command("seed_data")
    def create_user():

        db.create_all()

        user = User("tuncutku10@gmail.com", "1234")
        portfolio = Portfolio("My portfolio 1")
        position = Position(aapl)
        cost = SingleValue(120, aapl.asset_currency)
        order = Order(10, buy, cost, datetime(2020, 4, 1))

        # Save objects
        user.save_to_db()
        alert = user.add_market_alert(MarketAlert(PriceSignal(aapl, up, 300)))
        user.add_portfolio(portfolio)
        portfolio.add_position(position)
        position.add_order(order)

        # Activate objects
        user.confirm_user()
        portfolio.daily_report.activate()
        alert.activate()

    @app.cli.command("init_db")
    def init_db():
        """Init database."""

        db.create_all()

    @app.cli.command("clear_db")
    def clear_db():

        db.drop_all()
