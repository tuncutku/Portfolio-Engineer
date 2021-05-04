"""Home endpoints."""


from flask import Blueprint, render_template
from src.extensions import db


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def home():
    """Home."""
    return render_template("home.html")


@home_blueprint.before_app_first_request
def create_db():
    """Initiate database."""
    db.create_all()
