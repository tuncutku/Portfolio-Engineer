from flask import Blueprint, request, session, url_for, render_template, redirect
from src.extensions import db


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@home_blueprint.before_app_first_request
def create_db():
    db.create_all()
