from flask import Blueprint, request, session, url_for, render_template, redirect

from src.app.models import User, Portfolio
from src.app.models.utils import UserError, requires_login, requires_questrade_access
from lib.questrade.questrade import Questrade

portfolio_blueprint = Blueprint("portfolio", __name__)

@portfolio_blueprint.route("/list", methods=["GET", "POST", "PUT", "DELETE"])
@requires_login
@requires_questrade_access
def account_list():
    q = Questrade()
    portfolioList = User.portfolio_list(q)
    return render_template("portfolio/portfolio_list.html", portfolioList = portfolioList)


@portfolio_blueprint.route("/summary/<string:portfolio_id>/overview", methods=["GET"])
@requires_login
# @requires_questrade_access
def portfolio_overview(portfolio_id):
    p = Portfolio(int(portfolio_id))
    report = generate_portfolio_summary(p)
    return render_template("portfolio/portfolio_overview.html", report=report)