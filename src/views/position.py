"""Position endpoints."""

from flask import Blueprint, url_for, render_template, redirect
from flask_login import login_required, current_user
from datetime import datetime

from src.environment.portfolio import Portfolio
from src.environment.position import Position
from src.environment.order import Order, OrderSideType
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

    if position.is_open:
        open_quantity = position.quantity.sum()
        position.add_order(
            abs(open_quantity.item()),
            OrderSideType.Sell if open_quantity > 0 else OrderSideType.Buy,
            position.security.value.value,
            datetime.now(),
        )

    return redirect(url_for("portfolio.list_portfolios"))
