from flask import Blueprint, request, session, url_for, render_template, redirect
from src.app.models import User
from src.app.models.utils import UserError


questrade_blueprint = Blueprint("questrade", __name__)


@questrade_blueprint.route("/access_code", methods=["GET", "POST"])
def insert_refresh_token():
    error_message = None
    if request.method == "POST":
        token = request.form["token"]
        try:
            if User.register_user(email, password):
                session["email"] = email
                return redirect(url_for(".portfolio"))
        except Exception as e:
            error_message = e.message
            return render_template("portfolio/questrade/token.html", error_message=error_message)
    return render_template("portfolio/questrade/token.html", error_message=error_message)
