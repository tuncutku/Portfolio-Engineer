from flask import Blueprint, request, session, url_for, render_template, redirect

from src.app.models import User
from src.app.models.utils import UserError
from lib.questrade import Questrade


questrade_blueprint = Blueprint("questrade", __name__)


@questrade_blueprint.route("/access_code", methods=["GET", "POST"])
def insert_refresh_token():
    error_message = None
    if request.method == "POST":
        token = request.form["token"]
        q = Questrade()
        try:
            # q.submit_refresh_token(token)
            return redirect(url_for("questrade.portfolio_list"))
        except:
            error_message = "Access Denied"
            return render_template("portfolio/questrade/token.html", error_message=error_message)
    return render_template("portfolio/questrade/token.html", error_message=error_message)
