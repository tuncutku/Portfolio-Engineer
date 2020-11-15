from flask import Blueprint, request, session, url_for, render_template, redirect

from src.app.models import User
from src.app.models.utils import UserError, requires_login, requires_questrade_access
from lib.questrade.questrade import Questrade

portfolio_blueprint = Blueprint("portfolio", __name__)

@portfolio_blueprint.route("/list", methods=["GET", "POST", "PUT", "DELETE"])
@requires_login
@requires_questrade_access
def account_list():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        try:
            if User.register_user(email, password):
                session["email"] = email
                return redirect(url_for(".portfolio"))
        except UserError as e:
            return e.message
    
    q = Questrade()
    portfolioList = User.portfolio_list(q)
    return render_template("portfolio/portfolio_list.html", portfolioList = portfolioList)


@portfolio_blueprint.route("/summary", methods=["GET", "POST"])
@requires_login
@requires_questrade_access
def portfolio_overview():
    # if request.method == "POST":
    #     email = request.form["email"]
    #     password = request.form["password"]

    #     try:
    #         if User.register_user(email, password):
    #             session["email"] = email
    #             return redirect(url_for(".portfolio"))
    #     except UserError as e:
    #         return e.message
    return render_template("portfolio/portfolio_overview.html")