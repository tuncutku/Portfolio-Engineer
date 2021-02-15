from flask import Blueprint, url_for, render_template, redirect
from flask_login import login_required, current_user
import pandas as pd
import collections

from src.environment.user_activities.portfolio import Portfolio
from src.environment.user_activities.position import Position
from src.forms.portfolio_forms import AddPortfolioForm, generate_edit_portfolio_form
from src.extensions import db


portfolio_blueprint = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@portfolio_blueprint.route("/list", methods=["GET"])
@login_required
def list_portfolios():

    error_message = None
    port_list = [portfolio.to_dict() for portfolio in current_user.portfolios]
    port_list.sort(key=lambda x: x.get("Primary"), reverse=True)

    if not port_list:
        error_message = "Add a custom portfolio!"

    return render_template(
        "portfolio/list_portfolios.html",
        port_list=port_list,
        error_message=error_message,
    )


@portfolio_blueprint.route("/add_portfolio", methods=["GET", "POST"])
@login_required
def add_portfolio():

    form = AddPortfolioForm()
    if form.validate_on_submit():
        new_portfolio = Portfolio(
            name=form.port_name.data,
            portfolio_type=form.port_type.data,
            reporting_currency=form.port_reporting_currency.data,
            user=current_user,
        )
        new_portfolio.save_to_db()
        return redirect(url_for("portfolio.list_portfolios"))
    return render_template("portfolio/add_portfolio.html", form=form)


@portfolio_blueprint.route("/edit/<int:portfolio_id>", methods=["GET", "POST"])
@login_required
def edit_portfolio(portfolio_id):
    port = Portfolio.find_by_id(portfolio_id)
    form = generate_edit_portfolio_form(port)
    if form.validate_on_submit():
        port.edit(
            form.port_name.data, form.port_reporting_currency.data, form.port_type.data
        )
        return redirect(url_for("portfolio.list_portfolios"))
    return render_template(
        "portfolio/edit_portfolio.html", form=form, portfolio_id=portfolio_id
    )


@portfolio_blueprint.route("/delete/<int:portfolio_id>", methods=["GET"])
@login_required
def delete_portfolio(portfolio_id):
    port = Portfolio.find_by_id(portfolio_id)
    port.delete_from_db()
    return redirect(url_for("portfolio.list_portfolios"))


@portfolio_blueprint.route("/set_primary/<int:portfolio_id>", methods=["GET"])
@login_required
def set_portfolio_primary(portfolio_id):

    primary_portfolio = Portfolio.query.filter_by(
        user=current_user, is_primary=True
    ).first()

    if primary_portfolio:
        primary_portfolio.is_primary = False

    current_portfolio = Portfolio.find_by_id(portfolio_id)
    current_portfolio.set_as_primary()

    return redirect(url_for("portfolio.list_portfolios"))


# @portfolio_blueprint.route("/update", methods=["GET"])
# @login_required
# @requires_questrade_access
# def update_portfolio_list(q: Questrade):

#     # List the Questrade portfolios saved in database, and pulled Questrade portfolios
#     port_list_questrade = [port for port in q.accounts["accounts"]]
#     port_list_db = [
#         port
#         for port in Portfolio.find_all(session["email"])
#         if port.source == "Questrade"
#     ]
#     port_id_list_db = [port.questrade_id for port in port_list_db]

#     # Insert a new portfolio or update an existing portfolio
#     for port_questrade in port_list_questrade:
#         port_id = int(port_questrade["number"])
#         if port_id in port_id_list_db:
#             # Get Portfolio by Questrade id
#             port_db = port_list_db[port_id_list_db.index(port_id)]
#             check_and_update_portfolio(port_db, port_questrade)
#         else:
#             _add_portfolio(port_questrade, session["email"])

#     # TODO: add functionality to delete portfolios if it doesn't exist on Questrade

#     return redirect(url_for("portfolio.list_portfolios"))