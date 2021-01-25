from flask import Blueprint, request, session, url_for, render_template, redirect
import datetime

from src.environment.user_activities import Position, Portfolio, Order
from src.views.utils import (
    requires_login,
    market_data_connection,
    _modify_position_list,
    _check_position_validity,
    _extract_open_orders,
    _validate_order,
    _get_exec_time,
)
from src.views.errors.user_level_errors import UserLevelError
from src.questrade import Questrade_Market_Data
from src.questrade.utils import InvalidSymbolError
from src.views.utils.common import get_quote_from_symbol


order_blueprint = Blueprint("order", __name__)


@order_blueprint.route(
    "/<string:portfolio_name>/view_orders/<string:symbol>/", methods=["GET"]
)
@requires_login
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
@requires_login
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
@requires_login
@market_data_connection
def edit_order(
    md: Questrade_Market_Data, portfolio_name: str, symbol: str, order_id: int
):

    port = Portfolio.find_by_name(portfolio_name, session["email"])
    order = Order.find_by_id(order_id)
    if request.method == "POST":
        try:
            _validate_order(dict(request.form), md)
        except (InvalidSymbolError, UserLevelError) as e:
            return render_template(
                "order/edit_order.html",
                portfolio=port,
                order=order,
                required_amount=None,
                error_message=e.message,
            )

        exec_datetime = _get_exec_time(request.form["date"], request.form["time"])
        quote = get_quote_from_symbol(request.form["symbol"], md)
        position = Position.find_by_symbol(symbol, port.portfolio_id)

        order.update_order(
            symbol,
            "Custom",
            "Executed",
            int(request.form["order_quantity"]),
            request.form["order_type"],
            quote,
            exec_datetime,
            request.form["strategy"],
            port.portfolio_id,
            float(request.form["fee"]),
            position.position_id,
        )

        if port.source == "Questrade":
            return redirect(
                url_for("position.sync_position_list", portfolio_name=portfolio_name)
            )
        else:
            return redirect(
                url_for(
                    "position.update_position",
                    portfolio_name=portfolio_name,
                    symbol=symbol,
                )
            )

    return render_template(
        "order/edit_order.html",
        portfolio=port,
        order=order,
        required_amount=None,
        error_message=None,
    )


# TODO: required_amount can be negative (which means the position is "sell", fix it!)
@order_blueprint.route(
    "/<string:portfolio_name>/add_order/<string:symbol>/<float:required_amount>/",
    methods=["GET", "POST"],
)
@order_blueprint.route("/<string:portfolio_name>/add_order/", methods=["GET", "POST"])
@requires_login
@market_data_connection
def add_order(
    md: Questrade_Market_Data,
    portfolio_name: str,
    symbol: str = None,
    required_amount: int = None,
):
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    if request.method == "POST":
        try:
            _validate_order(dict(request.form), md)
        except (InvalidSymbolError, UserLevelError) as e:
            return render_template(
                "order/add_order.html",
                portfolio=port,
                symbol=symbol,
                required_amount=required_amount,
                error_message=e.message,
            )

        exec_datetime = _get_exec_time(request.form["date"], request.form["time"])
        quote = get_quote_from_symbol(request.form["symbol"], md)
        position_id = (
            Position.find_by_symbol(symbol, port.portfolio_id).position_id
            if symbol
            else None
        )

        Order.add_order(
            request.form["symbol"],
            "Custom",
            "Executed",
            float(request.form["order_quantity"]),
            request.form["order_type"],
            quote,
            exec_datetime,
            request.form["strategy"],
            port.portfolio_id,
            float(request.form["fee"]),
            position_id,
        )

        if port.source == "Custom":
            return redirect(
                url_for(
                    "position.update_position",
                    portfolio_name=portfolio_name,
                    symbol=request.form["symbol"],
                )
            )

        return redirect(
            url_for("position.sync_position_list", portfolio_name=portfolio_name)
        )

    return render_template(
        "order/add_order.html",
        portfolio=port,
        symbol=symbol,
        required_amount=required_amount,
        error_message=None,
    )
