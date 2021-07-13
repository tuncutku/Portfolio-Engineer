"""CLI"""


from datetime import datetime

import click
from flask import Blueprint
from src.extensions import db

from src.environment import User, Portfolio, Position, Order, MarketAlert
from src.market import SingleValue
from src.market.ref_data import aapl, buy, up
from src.market.signal import PriceSignal

cli_blueprint = Blueprint("cli", __name__, cli_group=None)


@cli_blueprint.cli.command("list_users")
def list_users():
    """List users."""

    for user in User.find_all():
        email = user.email
        n_portfolios = len(user.portfolios)
        click.echo(f"""User: {email} --> number of portfolios: {n_portfolios}""")


@cli_blueprint.cli.command("add_user")
@click.option("--email", prompt="Enter user email")
@click.option("--password", prompt="Enter user password")
def add_user(email, password):
    """List users."""

    if User.find_by_email(email):
        raise click.BadParameter("Email already exists in the database.")
    User(email, password, True).save_to_db()
    click.echo(f"User with the email: {email} added in to the database.")


@cli_blueprint.cli.command("seed_data")
def seed_data():
    """Seed sample emvironment data."""

    db.create_all()
    click.echo("Database created.")

    user = User("tuncutku10@gmail.com", "1234", True)
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
    portfolio.daily_report.activate()
    alert.activate()
    click.echo("Sample objects added into the database.")
    click.echo("Task completed.")


@cli_blueprint.cli.command("init_db")
def init_db():
    """Init database."""

    click.echo("Initializing database.")
    db.create_all()
    click.echo("Task completed.")


@cli_blueprint.cli.command("clear_db")
def clear_db():
    """Clear database."""

    click.echo("Dropping database.")
    db.drop_all()
    click.echo("Task completed.")
