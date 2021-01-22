from typing import List

from src.environment.user_activities.position import Position
from src.environment.user_activities.order import Order


def _modify_position_list(positions_questrade: list, positions_db: list):
    """Modify a list of dictionaries so that the keys will be symbols."""

    questrade_positions_dict = {
        position["symbol"]: position["openQuantity"] for position in positions_questrade
    }
    db_positions_dict_open = {
        position.symbol: position.quantity
        for position in positions_db
        if position.state == "Open"
    }
    db_positions_dict_closed = {
        position.symbol: position.quantity
        for position in positions_db
        if position.state == "Closed"
    }

    return questrade_positions_dict, db_positions_dict_open, db_positions_dict_closed


def _check_position_validity(positions: List[Position]) -> dict:
    """Check if sum of order amount verifies the position amount."""

    deficient_positions = dict()
    for position in positions:
        orders = Order.find_all(position_id=position.position_id)
        if orders:
            total_position_quantity = _sum_order_quantities(orders)
            if position.quantity != total_position_quantity:
                deficient_positions[position.symbol] = (
                    position.quantity - total_position_quantity
                )
        else:
            deficient_positions[position.symbol] = position.quantity
    return deficient_positions


def _sum_order_quantities(orders: list) -> float:
    return sum(
        [
            order.filledQuantity if order.side == "Buy" else order.filledQuantity * -1
            for order in orders
        ]
    )
