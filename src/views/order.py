from flask import Blueprint, request, session, url_for, render_template, redirect
from flask_login import login_required, current_user
import datetime

from src.extensions import db
from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order

from src.forms.order_forms import AddOrderForm, generate_edit_order_form

from src.market_data.yahoo import YFinance


order_blueprint = Blueprint("order", __name__, url_prefix="/order")


@order_blueprint.route(
    "/delete_order/<int:order_id>",
    methods=["GET"],
)
@login_required
def delete_order(order_id: int):

    order = Order.find_by_id(order_id)
    order.delete_from_db()

    return redirect(url_for("portfolio.list_portfolios"))


@order_blueprint.route(
    "/edit/<int:order_id>",
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
        return redirect(url_for("portfolio.list_portfolios"))

    return render_template("order/edit_order.html", form=form, order_id=order_id)


@order_blueprint.route("/<int:portfolio_id>/add_order", methods=["GET", "POST"])
@login_required
def add_order(portfolio_id):

    form = AddOrderForm()
    if form.validate_on_submit():
        symbol = form.symbol.data

        port = Portfolio.find_by_id(portfolio_id)
        pos = Position.query.filter_by(symbol=form.symbol.data, portfolio=port).first()
        if pos is None:
            md_provider = YFinance(symbol)
            symbol_info = md_provider.info()

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
