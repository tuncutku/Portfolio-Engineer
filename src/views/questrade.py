from flask import Blueprint, request, session, url_for, render_template, redirect

from src.environment.user_activities.auth import Auth
from src.environment.user_activities.utils import UserError, requires_login
from src.services.questrade.utils import InvalidTokenError
from src.services.questrade import Questrade

questrade_blueprint = Blueprint("questrade", __name__)

@questrade_blueprint.route("/access_code", methods=["GET", "POST"])
@requires_login
def insert_refresh_token():
    if request.method == "POST":
        token = request.form["token"]
        q = Questrade()
        try:
            q.submit_refresh_token(token)
            return redirect(url_for("account.list_portfolios"))
        except InvalidTokenError as e:
            return render_template("portfolio/questrade/token.html", error_message=e.message)
    return render_template("portfolio/questrade/token.html", error_message=None)