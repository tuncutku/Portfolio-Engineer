from flask import Blueprint, request, session, url_for, render_template, redirect
from flask_login import login_required, current_user
import datetime
import pandas as pd
import yfinance as yf

from src.environment.user_activities import Position, Portfolio, Order
from src.extensions import db
from src.forms.order_forms import AddOrderForm, generate_edit_order_form


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
    "/delete_order/<int:order_id>/",
    methods=["GET"],
)
@login_required
def delete_order(order_id: int):

    order = Order.find_by_id(order_id)
    order.delete_from_db()

    return redirect(url_for("portfolio.list_portfolios"))


@order_blueprint.route(
    "/edit_order/<int:order_id>/",
    methods=["GET", "POST"],
)
@login_required
def edit_order(order_id: int):
    order = Order.find_by_id(order_id)
    form = generate_edit_order_form(order)

    if form.validate_on_submit():
        order.edit(
            symbol=form.symbol.data,
            quantity=form.quantity.data,
            side=form.side.data,
            avg_exec_price=form.price.data,
            exec_time=form.exec_datetime.data,
            fee=form.fee.data,
        )
        return render_template(
            "position/position_details.html",
            position=order.position.to_dict(),
        )

    return render_template("order/edit_order.html", form=form, order_id=order_id)


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
