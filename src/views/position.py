# TODO: change the name of this file to position
from flask import Blueprint, request, session, url_for, render_template, redirect

from src.environment.user_activities import Position, Portfolio, Order
from src.views.utils import (
    requires_login,
    requires_questrade_access,
    market_data_connection,
)
from src.views.utils import (
    _modify_position_list,
    _check_position_validity,
    _update_order_id,
    _extend_position_list_with_md,
)

from src.questrade import Questrade, Questrade_Market_Data

position_blueprint = Blueprint("position", __name__, url_prefix="/position")

# TODO: Enable user to sort the positions by -> Amount, price, date etc.
@position_blueprint.route("/<string:portfolio_name>", methods=["GET"])
@requires_login
@market_data_connection
def list_positions(md: Questrade_Market_Data, portfolio_name: str):

    # TODO: Validate if the postiions are backed by orders
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    position_list = Position.find_all(port.portfolio_id)

    if position_list:
        # Add price and market cap to position list
        position_list = _extend_position_list_with_md(md, position_list)
        return render_template(
            "position/positions.html",
            position_list=position_list,
            portfolio=port,
            error_message=None,
        )
    else:
        if port.source == "Questrade":
            error_message = "You currently don't have any position. Time to sync orders with Questrade!"
        else:
            error_message = (
                "You currently don't have any position. Time to add new order!"
            )
        return render_template(
            "position/positions.html",
            position_list=position_list,
            portfolio=port,
            error_message=error_message,
        )


@position_blueprint.route("/sync/<string:portfolio_name>/", methods=["GET"])
@requires_login
@requires_questrade_access
def sync_position_list(q: Questrade, portfolio_name: str):

    port = Portfolio.find_by_name(portfolio_name, session["email"])
    port_id = port.portfolio_id

    (
        position_dict_questrade,
        position_dict_db_open,
        position_dict_db_closed,
    ) = _modify_position_list(
        q.account_positions(port.questrade_id)["positions"],
        Position.find_all(port_id),
    )

    position_set_questrade = set(position_dict_questrade.keys())
    position_set_db = set(position_dict_db_open.keys())

    # Find existing positions in Questrade
    for existing_position in list(position_set_questrade.intersection(position_set_db)):
        if (
            position_dict_questrade[existing_position]
            != position_dict_db_open[existing_position]
        ):
            position_db = Position.find_by_symbol(existing_position, port_id)
            position_db.update_position(
                position_dict_questrade[existing_position], "Open"
            )

    # Find deleted positions in Questrade
    for removed_position in list(position_set_db - position_set_questrade):
        position_db = Position.find_by_symbol(removed_position, port_id)
        position_db.update_position(0, "Closed")

    # Find new positions in Questrade
    for new_position in list(position_set_questrade - position_set_db):
        # Check if new position is a previously closed position
        if new_position in position_dict_db_closed:
            position_db = Position.find_by_symbol(new_position, port_id)
            position_db.update_position(position_dict_questrade[new_position], "Open")
        else:
            position = Position(
                new_position,
                "Questrade",
                position_dict_questrade[new_position],
                "Open",
                port_id,
            )
            position.add_position()

    deficient_positions = _check_position_validity(Position.find_all(port_id))
    if deficient_positions:
        return render_template(
            "position/incomplete_positions.html",
            deficient_positions=deficient_positions,
            portfolio=port,
        )

    return redirect(url_for("position.list_positions", portfolio_name=portfolio_name))


@position_blueprint.route(
    "/update/<string:portfolio_name>/<string:symbol>", methods=["GET"]
)
@requires_login
def update_position(portfolio_name: str, symbol: str):

    port = Portfolio.find_by_name(portfolio_name, session["email"])
    orders = Order.find_all_by_symbol(port.portfolio_id, symbol)
    position_generated = Position.generate_by_orders(orders, symbol, port.portfolio_id)

    try:
        position_db = Position.find_by_symbol(symbol, port.portfolio_id)
        position_db.update_position(position_generated.quantity)
    except:  # TODO: add a custom exception
        position_generated.add_position()
        position_db = Position.find_by_symbol(symbol, port.portfolio_id)
    _update_order_id(orders, position_db.position_id)

    if position_generated.quantity == 0:
        position_db.delete_position()

    return redirect(url_for("position.list_positions", portfolio_name=portfolio_name))


@position_blueprint.route(
    "/close_position/<string:portfolio_name>/<string:symbol>", methods=["GET"]
)
@requires_login
def close_position(portfolio_name: str, symbol: str):

    # port = Portfolio.find_by_name(portfolio_name, session["email"])
    # orders = Order.find_all_by_symbol(port.portfolio_id, symbol)
    # position_generated = Position.generate_by_orders(orders, symbol, port.portfolio_id)
    # position_db = Position.find_by_symbol(symbol, port.portfolio_id)

    # Order.add_order(
    #     request.form["symbol"],
    #     "Custom",
    #     "Executed",
    #     int(request.form["order_quantity"]),
    #     request.form["order_type"],
    #     33, # TODO: pull this from Market Data Manager
    #     exec_datetime,
    #     request.form["strategy"],
    #     port.portfolio_id,
    #     0,
    #     Position.find_by_symbol(symbol, port.portfolio_id).position_id if symbol else None,
    # )

    pass