import os

from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from flask_login import login_user, logout_user

from src.environment.user_activities import User
from src.forms.user_forms import RegisterForm, LoginForm
from src.extensions import db


user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user)
        flash("You have been logged in.", category="success")
        return redirect(url_for("portfolio.list_portfolios"))
    return render_template("user/login.html", form=form)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.email.data)
        new_user.set_password(form.password.data)
        # Add user to database
        new_user.save_to_db()
        return redirect(url_for("users.login"))
    return render_template("user/register.html", form=form)


@user_blueprint.route("/guest", methods=["GET", "POST"])
def guest():
    session["email"] = os.environ["GUEST_EMAIL"]
    return redirect(url_for("portfolio.list_portfolios"))


@user_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("You have been logged out.", category="success")
    return redirect(url_for("home"))
