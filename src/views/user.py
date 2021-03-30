import os

from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from flask_login import login_user, logout_user
from itsdangerous import URLSafeTimedSerializer

from src.environment.user import User
from src.forms.user_forms import RegisterForm, LoginForm
from src.extensions import db
from src.tasks.email import send_email


user_blueprint = Blueprint("users", __name__, url_prefix="/users")


@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user)
        return redirect(url_for("portfolio.list_portfolios"))
    return render_template("user/login.html", form=form)


@user_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(form.email.data)
        new_user.save_to_db()
        new_user.set_password(form.password.data)

        token = generate_confirmation_token(new_user.email)
        confirm_url = url_for("users.confirm_email", token=token, _external=True)
        email = {
            "subject": "Account confirmation - Portfolio Engineer",
            "recipient": [new_user.email],
            "html": render_template(
                "email/account_confirmation.html", confirm_url=confirm_url
            ),
        }
        send_email(email=email)

        flash("You have confirmed your account. Thanks!", "success")

        return redirect(url_for("users.login"))
    return render_template("user/register.html", form=form)


@user_blueprint.route("/confirm/<string:token>", methods=["GET"])
def confirm_email(token):
    email = confirm_token(token)

    if email:
        user = User.find_by_email(email)
        user.confirm_user()
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("users.login"))


@user_blueprint.route("/guest", methods=["GET", "POST"])
def guest():
    session["email"] = "Hey"
    return redirect(url_for("portfolio.list_portfolios"))


@user_blueprint.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("home.home"))


def generate_confirmation_token(email: str):
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    return serializer.dumps(email, salt=os.environ.get("SECURITY_PASSWORD_SALT"))


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))
    try:
        email = serializer.loads(
            token, salt=os.environ.get("SECURITY_PASSWORD_SALT"), max_age=expiration
        )
    except:
        return None
    return email
