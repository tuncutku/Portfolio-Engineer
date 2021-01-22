from flask import Blueprint, request, session, url_for, render_template, redirect

from src.environment.user_activities import Portfolio
from src.views.utils import requires_login, requires_questrade_access
from src.views.utils import (
    check_and_update_portfolio,
    _add_portfolio,
    _valide_portfolio_name,
)

from src.questrade import Questrade

account_blueprint = Blueprint("account", __name__)


@account_blueprint.route("/account", methods=["GET", "POST", "PUT", "DELETE"])
@requires_login
def list_portfolios():
    # TODO: add primary secondary portfolio - the website will list the primary first and will show the positions directly.
    port_list = Portfolio.find_all(session["email"])
    if port_list:
        return render_template(
            "account/account.html", port_list=port_list, error_message=None
        )
    else:
        error_message = "You currently don't have a portfolio. Add a custom portfolio or update with your Questrade account!"
        return render_template(
            "account/account.html", port_list=port_list, error_message=error_message
        )


@account_blueprint.route("/update", methods=["GET"])
@requires_login
@requires_questrade_access
def update_portfolio_list(q: Questrade):

    # List the Questrade portfolios saved in database, and pulled Questrade portfolios
    port_list_questrade = [port for port in q.accounts["accounts"]]
    port_list_db = [
        port
        for port in Portfolio.find_all(session["email"])
        if port.source == "Questrade"
    ]
    port_id_list_db = [port.questrade_id for port in port_list_db]

    # Insert a new portfolio or update an existing portfolio
    for port_questrade in port_list_questrade:
        port_id = int(port_questrade["number"])
        if port_id in port_id_list_db:
            # Get Portfolio by Questrade id
            port_db = port_list_db[port_id_list_db.index(port_id)]
            check_and_update_portfolio(port_db, port_questrade)
        else:
            _add_portfolio(port_questrade, session["email"])

    # TODO: add functionality to delete portfolios if it doesn't exist on Questrade

    return redirect(url_for("account.list_portfolios"))


@account_blueprint.route(
    "/delete/<string:portfolio_name>", methods=["GET", "POST", "PUT", "DELETE"]
)
@requires_login
def delete_portfolio(portfolio_name):
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    # TODO:Orders and positions should be deleted too.
    port.delete_portfolio()
    return redirect(url_for("account.list_portfolios"))


@account_blueprint.route("/portfolio_name", methods=["GET", "POST"])
@requires_login
def add_portfolio():
    if request.method == "POST":
        name = request.form["name"]
        if not _valide_portfolio_name(name, session["email"]):
            error_message = f"Invalid name! A portfolio named '{name}' already exists."
            return render_template(
                "account/add_portfolio.html", error_message=error_message
            )
        else:
            # Portfolio type can be specified my the user. Add a drop down menu.
            Portfolio.add_portfolio(
                name, "Custom", "Active", "Invalid", session["email"]
            )
            return redirect(url_for("account.list_portfolios"))
    return render_template("account/add_portfolio.html", error_message=None)


@account_blueprint.route("/edit/<string:portfolio_name>", methods=["GET", "POST"])
@requires_login
def edit_portfolio(portfolio_name):
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    if request.method == "POST":
        name = request.form["name"]
        status = request.form["portfolio_status"]
        port_type = request.form["portfolio_type"]

        if (
            name == port.name
            and status == port.status
            and port_type == port.portfolio_type
        ):
            error_message = "Your current portfolio has the same attributes!"
            return render_template(
                "account/edit_portfolio.html",
                portfolio=port,
                error_message=error_message,
            )
        if not _valide_portfolio_name(name, session["email"]) and name != port.name:
            error_message = f"Invalid name! A portfolio named '{name}' already exists."
            return render_template(
                "account/edit_portfolio.html",
                portfolio=port,
                error_message=error_message,
            )
        else:
            # Portfolio type can be specified my the user. Add a drop down menu.
            port.update_portfolio(name, status, port_type)
            return redirect(url_for("account.list_portfolios"))
    return render_template(
        "account/edit_portfolio.html", portfolio=port, error_message=None
    )
