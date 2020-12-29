from flask import Blueprint, request, session, url_for, render_template, redirect
import datetime

from src.environment.user_activities import Position, Portfolio, Order
from src.views.utils import requires_login, _modify_position_list, _check_position_validity, _extract_open_orders


order_blueprint = Blueprint("order", __name__)


@order_blueprint.route("/<string:portfolio_name>/view_orders/<string:symbol>/", methods=["GET"])
@requires_login
def list_orders(portfolio_name: str, symbol: str):
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    position = Position.find_by_symbol(symbol, port.portfolio_id)
    all_orders = Order.find_all(position.position_id)
    open_orders = _extract_open_orders(all_orders)
    return render_template("order/order.html", symbol=position.symbol, order_list=open_orders, portfolio=port)

@order_blueprint.route("/<string:portfolio_name>/add_order/<string:symbol>/<int:required_amount>/", methods=["GET", "POST"])
@order_blueprint.route("/<string:portfolio_name>/add_order/<string:symbol>/", methods=["GET", "POST"])
@requires_login
def add_order(portfolio_name: str, symbol: str, required_amount: int = None):
    port = Portfolio.find_by_name(portfolio_name, session["email"])
    if request.method == "POST":
        try:
            date = datetime.datetime.strptime(request.form["date"], "%Y-%m-%d")
            time = datetime.datetime.strptime(request.form["time"], "%H:%M").time()
        except ValueError: # Add exception
            return render_template(
                "order/add_order.html",
                portfolio=port,
                symbol=symbol,
                required_amount=required_amount,
                error_message = "Invalid date or time provided, please try again."
            )
        
        exec_datetime = datetime.datetime.combine(date, time)
        position = Position.find_by_symbol(symbol, port.portfolio_id)

        if request.form["fee-currency"] == "USD":
            pass # TODO: convert to CAD by using exchange rate


        Order.add_order(
            symbol,
            "Custom",
            "Executed",
            int(request.form["order_quantity"]),
            request.form["order_type"],
            33, # TODO: pull this from Market Data Manager
            exec_datetime,
            request.form["strategy"],
            port.portfolio_id,
            float(request.form["fee"]),
            position.position_id,
        )

        return redirect(url_for("portfolio.update_position_list", portfolio_name=portfolio_name))


    return render_template(
        "order/add_order.html",
        portfolio=port,
        symbol=symbol,
        required_amount=required_amount,
        error_message = None
    )
