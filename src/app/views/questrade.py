from flask import Blueprint, request, session, url_for, render_template, redirect

from src.app.models.auth import Auth
from src.app.models.utils import UserError, requires_login
from lib.questrade.utils import WrongTokenError
from lib.questrade import Questrade


questrade_blueprint = Blueprint("questrade", __name__)

@questrade_blueprint.route("/access_code", methods=["GET", "POST"])
@requires_login
def insert_refresh_token():
    if request.method == "POST":
        token = request.form["token"]
        q = Questrade()
        try:
            q.submit_refresh_token(token)
            return redirect(url_for("questrade.account_list"))
        except WrongTokenError as e:
            return render_template("portfolio/questrade/token.html", error_message=e.message)
    return render_template("portfolio/questrade/token.html", error_message=None)
