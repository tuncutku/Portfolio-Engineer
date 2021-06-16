"""User endpoints"""

# pylint: disable=no-value-for-parameter, bare-except
import os

from flask import Blueprint, url_for, render_template, redirect, flash
from flask_login import login_user, logout_user
from itsdangerous import URLSafeTimedSerializer

from src.environment.user import User
from src.forms.user import RegisterForm, LoginForm
from src.tasks.email import send_email


user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Log in user."""
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        login_user(user)
        return redirect(url_for("portfolio.list_portfolios"))
    return render_template("user/login.html", form=form)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Register user and send a confirmation email."""
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.email.data, form.password.data)
        new_user.save_to_db()

        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for("users.confirm_email", token=token, _external=True)

        send_email(
            subject="Account confirmation - Portfolio Engineer",
            recipients=[new_user.email],
            html=render_template(
                "email/account_confirmation.html", confirm_url=confirm_url
            ),
        )

        flash("You have confirmed your account. Thanks!", "success")
        return redirect(url_for("users.login"))
    return render_template("user/register.html", form=form)


@user_blueprint.route("/confirm/<string:token>", methods=["GET"])
def confirm_email(token):
    """Confirm user."""
    email = confirm_token(token)

    if email:
        user = User.find_by_email(email)
        user.confirm_user()
        user.save_to_db()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("users.login"))


@user_blueprint.route("/guest", methods=["GET", "POST"])
def guest():
    """Guest user."""
    login_user(User.find_by_email("guest_user@gmail.com"))
    return redirect(url_for("portfolio.list_portfolios"))


@user_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    """Log out user."""
    logout_user()
    return redirect(url_for("home.home"))


def generate_confirmation_token(email: str) -> str:
    """Generate token to be sent to the new user for registering."""
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    return serializer.dumps(email, salt=os.environ.get("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    """Use serializer to parse the token and to confirm the new user."""
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    try:
        email = serializer.loads(
            token, salt=os.environ.get("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
    except:
        return None
    return email
