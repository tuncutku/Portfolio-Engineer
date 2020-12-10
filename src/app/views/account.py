from flask import Blueprint, request, session, url_for, render_template, redirect

from src.app.models import User, Portfolio
from src.app.models.utils import UserError, requires_login, requires_questrade_access, PortfolioNotFoundError
from lib.questrade.questrade import Questrade

account_blueprint = Blueprint("account", __name__)

@account_blueprint.route("/list", methods=["GET", "POST", "PUT", "DELETE"])
@requires_login
def portfolio_list():
    try:
        port_list = Portfolio.find_all(session["email"])
        return render_template("portfolio/portfolio_list.html", port_list = port_list, error_message = None)
    except PortfolioNotFoundError as e:
        port_list = None
        return render_template("portfolio/portfolio_list.html", port_list = port_list, error_message = e.message)

@account_blueprint.route("/update", methods=["GET", "POST", "PUT", "DELETE"])
@requires_login
@requires_questrade_access
def update_portfolio_list():
    q = Questrade
    q.accounts
    return None

@account_blueprint.route("/update", methods=["GET", "POST", "PUT", "DELETE"])
@requires_login
def edit_portfolio():
    pass

@account_blueprint.route("/update", methods=["GET", "POST", "PUT", "DELETE"])
@requires_login
def delete_portfolio():
    pass
