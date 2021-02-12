from flask import Blueprint, request, session, url_for, render_template, redirect
from flask_login import login_required, current_user
import datetime
import pandas as pd
import yfinance as yf

from src.environment.user_activities import Position, Portfolio, Order
from src.extensions import db
from src.forms.order_forms import AddOrderForm


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
def edit_order(md, portfolio_name: str, symbol: str, order_id: int):
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
        symbol = form.symbol.data

        port = Portfolio.find_by_id(portfolio_id)
        pos = Position.query.filter_by(symbol=form.symbol.data, portfolio=port).first()
        if pos is None:
            symbol_info = yf.Ticker(symbol).info
            pos = Position(
                symbol=symbol,
                name=symbol_info.get("shortName", None),
                security_type=symbol_info.get("quoteType", None),
                currency=symbol_info.get("currency", None),
                portfolio=port,
            )
            pos.save_to_db()

        new_order = Order(
            symbol=form.symbol.data,
            quantity=form.quantity.data,
            side=form.side.data,
            avg_exec_price=form.price.data,
            exec_time=form.exec_datetime.data,
            fee=form.fee.data,
            position=pos,
        )

        new_order.save_to_db()

        return redirect(url_for("portfolio.list_portfolios"))

    return render_template("order/add_order.html", form=form, portfolio_id=portfolio_id)
