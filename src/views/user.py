import os

from flask import Blueprint, request, session, url_for, render_template, redirect
from src.models import User
from src.models.utils import UserError


# TODO integrate "LoginManager() for managing logins"
user_blueprint = Blueprint("users", __name__)

@user_blueprint.route("/login", methods=["GET", "POST"])
def login_user():
    error_message = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            if User.is_login_valid(email, password):
                session["email"] = email
                return redirect(url_for("account.list_portfolios"))
        except UserError as e:
            error_message = e.message
            return render_template("users/login.html", error_message=error_message)
    return render_template("users/login.html", error_message=error_message)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            if User.register_user(email, password):
                session["email"] = email
                return redirect(url_for("account.list_portfolios"))
        except UserError as e:
            return e.message
    return render_template("users/register.html")


@user_blueprint.route("/guest", methods=["GET", "POST"])
def guest():
    session["email"] = os.environ["GUEST_EMAIL"]
    return redirect(url_for("account.list_portfolios"))

@user_blueprint.route("/logout", methods=["GET"])
def log_out_user():
    return render_template("home.html")

