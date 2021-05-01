"""Portfolio endpoints."""

from flask import Blueprint, url_for, render_template, redirect, flash
from flask_login import login_required, current_user
import pandas as pd
import collections

from src.environment import Portfolio
from src.market import Symbol
from src.forms.portfolio import AddPortfolioForm, generate_edit_portfolio_form
from src.views.utils.common import get_security

from src.extensions import db


portfolio_blueprint = Blueprint("portfolio", __name__, url_prefix="/portfolio")


@portfolio_blueprint.route("/list", methods=["GET"])
@login_required
def list_portfolios():
    """List portfolios of the user including current market values."""

    port_list = current_user.portfolios
    port_list.sort(key=lambda x: x.primary, reverse=True)
    port_list = []

    if not port_list:
        flash("Add a custom portfolio!")

    return render_template(
        "portfolio/list_portfolios.html",
        port_list=port_list,
    )


@portfolio_blueprint.route("/add_portfolio", methods=["GET", "POST"])
@login_required
def add_portfolio():
    """Add a new portfolio."""

    form = AddPortfolioForm()
    if form.validate_on_submit():

        symbol = Symbol(form.benchmark.data)
        security = get_security(symbol)

        portfolio = current_user.add_portfolio(
            form.port_name.data,
            form.port_type.data,
            form.port_reporting_currency.data,
            security,
        )
        if len(current_user.portfolios) == 1:
            portfolio.set_as_primary()
        return redirect(url_for("portfolio.list_portfolios"))
    return render_template("portfolio/add_portfolio.html", form=form)


@portfolio_blueprint.route("/edit/<int:portfolio_id>", methods=["GET", "POST"])
@login_required
def edit_portfolio(portfolio_id):
    """Edit an existing portfolio."""
    port = Portfolio.find_by_id(portfolio_id)
    form = generate_edit_portfolio_form(port)
    if form.validate_on_submit():
        port.edit(
            form.port_name.data,
            form.port_reporting_currency.data,
            form.port_type.data,
            form.benchmark.data,
        )
        return redirect(url_for("portfolio.list_portfolios"))
    return render_template(
        "portfolio/edit_portfolio.html", form=form, portfolio_id=portfolio_id
    )


@portfolio_blueprint.route("/delete/<int:portfolio_id>", methods=["GET"])
@login_required
def delete_portfolio(portfolio_id):
    """Delete an existing portfolio along with its positions as well as orders."""
    port = Portfolio.find_by_id(portfolio_id)
    port.delete_from_db()
    return redirect(url_for("portfolio.list_portfolios"))


@portfolio_blueprint.route("/set_primary/<int:portfolio_id>", methods=["GET"])
@login_required
def set_portfolio_primary(portfolio_id):
    """Set a portfolio primary which will be viewed at the top when listing portfolios."""

    primary_portfolio = Portfolio.get_primary(current_user)

    if primary_portfolio:
        primary_portfolio.primary = False

    current_portfolio = Portfolio.find_by_id(portfolio_id)
    current_portfolio.set_as_primary()

    return redirect(url_for("portfolio.list_portfolios"))
