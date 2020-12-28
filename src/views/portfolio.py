from flask import Blueprint, request, session, url_for, render_template, redirect

from src.environment.user_activities import Position, Portfolio
from src.views.utils import requires_login, requires_questrade_access
from src.views.utils import _modify_position_list, _check_position_validity

from src.questrade import Questrade

portfolio_blueprint = Blueprint("portfolio", __name__)

# TODO: Enable user to sort the positions by -> Amount, price, date etc.
@portfolio_blueprint.route("/<string:portfolio_name>", methods=["GET"])
@requires_login
def list_positions(portfolio_name: str):
    # TODO: Validate if the postiions are backed by orders
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    position_list = Position.find_all(port.portfolio_id)
    if position_list:
        return render_template("portfolio/portfolio.html", position_list = position_list, portfolio=port, error_message = None)
    else: 
        error_message = "You currently don't have any position. Time to add new orders! or pull them from Questrade."
        return render_template("portfolio/portfolio.html", position_list = position_list, portfolio=port, error_message = error_message)

@portfolio_blueprint.route("/update/<string:portfolio_name>/", methods=["GET"])
@requires_login
@requires_questrade_access
def update_position_list(q: Questrade, portfolio_name: str):

    port = Portfolio.find_by_name(portfolio_name, session["email"])
    port_id = port.portfolio_id

    position_dict_questrade, position_dict_db_open, position_dict_db_closed = _modify_position_list(
        q.account_positions(port.questrade_id)["positions"], 
        Position.find_all(port_id),
    )

    position_set_questrade = set(position_dict_questrade.keys())
    position_set_db = set(position_dict_db_open.keys())

    # Find existing positions in Questrade
    for existing_position in list(position_set_questrade.intersection(position_set_db)):
        if position_dict_questrade[existing_position] != position_dict_db_open[existing_position]:
            position_db = Position.find_by_symbol(existing_position, port_id)
            position_db.update_position(position_dict_questrade[existing_position], "Open")

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
            Position.add_position(new_position, "Questrade", position_dict_questrade[new_position], port_id)
    
    deficient_positions = _check_position_validity(Position.find_all(port_id))
    if deficient_positions:
        return render_template("portfolio/incomplete_positions.html", deficient_positions=deficient_positions, portfolio=port)

    return redirect(url_for("portfolio.list_positions", portfolio_name=portfolio_name))

@portfolio_blueprint.route("/<string:portfolio_name>/edit_position/<string:symbol>/", methods=["GET", "POST"])
@requires_login
def add_position(portfolio_name: str, symbol: str):
    if request.method == "POST":
        pass

    a = 1

    return 4