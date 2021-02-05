from flask import Blueprint, request, session, url_for, render_template, redirect
from flask_login import login_required, current_user
import datetime

import inspect

from collections import defaultdict

from src.environment.user_activities import Position, Portfolio
from src.environment.user_activities.order import Order
from src.views.utils import (
    requires_login,
    market_data_connection,
    _modify_position_list,
    _check_position_validity,
    _extract_open_orders,
    _validate_order,
    _get_exec_time,
)
from src import db_1
from src.views.errors.user_level_errors import UserLevelError
from src.questrade import Questrade_Market_Data
from src.questrade.utils import InvalidSymbolError
from src.views.utils.common import get_quote_from_symbol

from src.forms.order_forms import AddOrderForm

import pandas as pd


order_blueprint = Blueprint("order", __name__, url_prefix="/order")


@order_blueprint.route(
    "/<string:portfolio_name>/view_orders/<string:symbol>/", methods=["GET"]
)
@login_required
def list_orders(portfolio_name: str, symbol: str):
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    position = Position.find_by_symbol(symbol, port.portfolio_id)
    all_orders = Order.find_all(position_id=position.position_id)
    open_orders = _extract_open_orders(all_orders)
    return render_template(
        "order/order.html",
        portfolio_name=portfolio_name,
        symbol=position.symbol,
        order_list=open_orders,
        portfolio=port,
    )


@order_blueprint.route(
    "/<string:portfolio_name>/delete_order/<string:symbol>/<int:order_id>/",
    methods=["GET"],
)
@login_required
def delete_order(portfolio_name: str, symbol: str, order_id: int):
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    order = Order.find_by_id(order_id)
    order.delete_order()
    if port.source == "Questrade":
        return redirect(
            url_for("position.sync_position_list", portfolio_name=portfolio_name)
        )
    else:
        return redirect(
            url_for(
                "position.update_position", portfolio_name=portfolio_name, symbol=symbol
            )
        )


@order_blueprint.route(
    "/<string:portfolio_name>/edit_order/<string:symbol>/<int:order_id>/",
    methods=["GET", "POST"],
)
@login_required
def edit_order(
    md: Questrade_Market_Data, portfolio_name: str, symbol: str, order_id: int
):
    form = generate_edit_portfolio_form(port)

    return render_template(
        "order/edit_order.html",
        portfolio=port,
        order=order,
        required_amount=None,
        error_message=None,
    )


# TODO: required_amount can be negative (which means the position is "sell", fix it!)
@order_blueprint.route("/<int:portfolio_id>/add_order/", methods=["GET", "POST"])
@login_required
def add_order(portfolio_id):

    form = AddOrderForm()
    if form.validate_on_submit():
        new_order = Order(
            form.symbol.data,
            form.quantity.data,
            form.side.data,
            form.price.data,
            form.exec_datetime.data,
            form.fee.data,
        )
        new_order.portfolio_id = portfolio_id
        db_1.session.add(new_order)
        db_1.session.commit()

        return redirect(url_for("portfolio.list_portfolios"))

    return render_template("order/add_order.html", form=form, portfolio_id=portfolio_id)
