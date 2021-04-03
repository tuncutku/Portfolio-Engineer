from flask import Blueprint, url_for, render_template, redirect
from flask_login import login_required, current_user
from datetime import datetime

from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order, OrderSideType
from src.forms.portfolio_forms import AddPortfolioForm, generate_edit_portfolio_form
from src.market_data.provider import YFinance
from src.extensions import db


position_blueprint = Blueprint("position", __name__, url_prefix="/position")


@position_blueprint.route("/<int:position_id>/details", methods=["GET"])
@login_required
def position_details(position_id):

    position = Position.find_by_id(position_id)

    return render_template(
        "position/position_details.html",
        position=position.to_dict(),
    )


@position_blueprint.route("/<int:position_id>/close", methods=["GET"])
@login_required
def close_position(position_id):

    position = Position.find_by_id(position_id)

    if position.open:
        md_provider = YFinance([position.symbol])
        quote = md_provider.get_current_quotes(decimal=2)

        side = OrderSideType.Sell if position.open_quantity > 0 else OrderSideType.Buy

        order = Order(
            symbol=position.symbol,
            quantity=abs(position.open_quantity),
            side=side,
            exec_price=quote[position.symbol],
            exec_time=datetime.now(),
            fee=0,
            position=position,
        )
        order.save_to_db()

    return redirect(url_for("portfolio.list_portfolios"))
