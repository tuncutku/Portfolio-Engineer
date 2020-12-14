from flask import Blueprint, request, session, url_for, render_template, redirect

from src.app.models import User #Portfolio
from src.app.models.utils import UserError, requires_login, requires_questrade_access
from src.app.lib.questrade import Questrade

portfolio_blueprint = Blueprint("portfolio", __name__)


@portfolio_blueprint.route("/summary/<string:portfolio_id>/overview", methods=["GET"])
@requires_login
# @requires_questrade_access
def portfolio_overview(portfolio_id):
    p = Portfolio(int(portfolio_id))
    #report = generate_portfolio_summary(p)
    return render_template("portfolio/portfolio_overview.html")# report=report)

def edit_portfolio():
    pass