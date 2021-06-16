"""Home endpoints"""

from datetime import datetime
from flask import Blueprint, render_template

from src.extensions import db

from src.environment import User, Portfolio, Position, Order
from src.market import SingleValue
from src.market.ref_data import buy, usd_ccy, cad_ccy, aapl, ry_to


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def home():
    """Home."""
    return render_template("home.html")


@home_blueprint.before_app_first_request
def add_user_guest():
    """Add guest user data."""

    email = "guest_user@gmail.com"
    password = "1234"

    db.create_all()
    if not User.find_by_email(email):

        # Create objects
        user = User(email, password)
        portfolio = Portfolio("My portfolio 1")
        position_1 = Position(aapl)
        position_2 = Position(ry_to)
        order_1 = Order(10, buy, SingleValue(100, usd_ccy), datetime(2021, 1, 5))
        order_2 = Order(15, buy, SingleValue(100, cad_ccy), datetime(2021, 2, 15))

        # Link and save objects
        user.save_to_db()
        user.confirm_user()
        user.add_portfolio(portfolio)
        portfolio.add_position(position_1)
        portfolio.add_position(position_2)
        position_1.add_order(order_1)
        position_2.add_order(order_2)
