from flask import Blueprint, request, session, url_for, render_template, redirect
from flask_login import login_required, current_user
import pandas as pd

from src.environment.user_activities.portfolio import Portfolio, PortfolioTag
from src.views.utils.common import edit_list_order
from src.views.utils import requires_questrade_access
from src.views.utils import (
    check_and_update_portfolio,
    _add_portfolio,
    _valide_portfolio_name,
)
from src.reports.portfolio_reports import PortfolioReport

from src.questrade import Questrade
from src.forms.portfolio_forms import AddPortfolioForm, generate_edit_portfolio_form
from src import db_1


portfolio_blueprint = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@portfolio_blueprint.route("/list", methods=["GET"])
@login_required
def list_portfolios():

    error_message = None
    port_list = Portfolio.query.filter_by(user_id=current_user.id).all()

    report_list = [PortfolioReport(port) for port in port_list]

    if port_list:
        port_list = edit_list_order(port_list)
    else:
        error_message = "You currently don't have a portfolio. Add a custom portfolio or sync with your Questrade account!"

    return render_template(
        "portfolio/list_portfolios.html",
        port_list=port_list,
        portfolio_tag=PortfolioTag,
        error_message=error_message,
    )


@portfolio_blueprint.route("/add_portfolio", methods=["GET", "POST"])
@login_required
def add_portfolio():

    form = AddPortfolioForm()

    if form.validate_on_submit():

        new_portfolio = Portfolio(
            form.port_name.data,
            current_user.id,
            form.port_type.data,
            form.port_reporting_currency.data,
        )

        db_1.session.add(new_portfolio)
        db_1.session.commit()

        return redirect(url_for("portfolio.list_portfolios"))

    return render_template("portfolio/add_portfolio.html", form=form)


@portfolio_blueprint.route("/edit/<int:portfolio_id>", methods=["GET", "POST"])
@login_required
def edit_portfolio(portfolio_id):
    port = Portfolio.query.filter_by(id=portfolio_id).first()
    form = generate_edit_portfolio_form(port)
    if form.validate_on_submit():
        port.name = form.port_name.data
        port.reporting_currency = form.port_reporting_currency.data
        port.portfolio_type = form.port_type.data
        db_1.session.commit()
        return redirect(url_for("portfolio.list_portfolios"))
    return render_template(
        "portfolio/edit_portfolio.html", form=form, portfolio_id=portfolio_id
    )


@portfolio_blueprint.route("/delete/<int:portfolio_id>", methods=["GET"])
@login_required
def delete_portfolio(portfolio_id):
    Portfolio.query.filter_by(id=portfolio_id).delete()
    db_1.session.commit()
    return redirect(url_for("portfolio.list_portfolios"))


@portfolio_blueprint.route("/set_primary/<int:portfolio_id>", methods=["GET"])
@login_required
def set_portfolio_primary(portfolio_id):

    primary_portfolio = Portfolio.query.filter_by(
        user_id=current_user.id, portfolio_tag=PortfolioTag.primary
    ).first()

    if primary_portfolio:
        primary_portfolio.portfolio_tag = PortfolioTag.regular

    current_portfolio = Portfolio.query.filter_by(id=portfolio_id).first()
    current_portfolio.portfolio_tag = PortfolioTag.primary

    db_1.session.commit()
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