"""Position endpoints"""

from datetime import datetime, date
from flask import Blueprint, url_for, render_template, redirect
from flask_login import login_required

from src.views.utils.common import get_business_day
from src.environment import Position, Order
from src.market.types import OrderSideType


position_blueprint = Blueprint("position", __name__, url_prefix="/position")


@position_blueprint.route("/<int:position_id>/details", methods=["GET"])
@login_required
def position_details(position_id):
    """Get position details."""

    return render_template(
        "position/position_details.html",
        position=Position.find_by_id(position_id),
    )


@position_blueprint.route("/<int:position_id>/close", methods=["GET"])
@login_required
def close_position(position_id):
    """Close existing position by adding closing order."""

    position = Position.find_by_id(position_id)

    if position.is_open:
        order = Order(
            position.open_quantity,
            OrderSideType.Sell if position.open_quantity > 0 else OrderSideType.Buy,
            position.security.value.value,
            get_business_day(date.today()),
        )
        position.add_order(order)

    return redirect(url_for("portfolio.list_portfolios"))
