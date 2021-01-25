from typing import List
import datetime

from src.environment.user_activities import Order
from src.questrade import Questrade_Market_Data
from src.views.errors.user_level_errors import (
    InvalidOrderAmountError,
    InvalidOrderDateError,
    InvalidOrderFeeError,
)


def _extract_open_orders(order_list: List[Order]) -> List[Order]:
    remaining_amount = sum(
        [
            order.filledQuantity if order.side == "Buy" else order.filledQuantity * -1
            for order in order_list
        ]
    )
    open_orders = list()
    for order in reversed(order_list):
        open_orders.append(order)
        remaining_amount = remaining_amount - order.filledQuantity
        if remaining_amount == 0:
            break
    return open_orders


def _update_order_id(orders: list, position_id: int) -> None:
    for order in orders:
        if order.position_id is None:
            order.insert_position_id(position_id)


def _validate_order(request: dict, md: Questrade_Market_Data) -> None:
    # TODO: if currency is USD convert it to CAD
    if int(float(request["order_quantity"])) <= 0:
        raise InvalidOrderAmountError(
            "Order amount should be a positive integer number."
        )

    if int(request["fee"]) < 0:
        raise InvalidOrderFeeError("Order fee should be a positive number.")

    try:
        datetime.datetime.strptime(request["date"], "%Y-%m-%d")
        datetime.datetime.strptime(request["time"], "%H:%M")
    except ValueError:
        raise InvalidOrderDateError("Incorrect date format.")

    md.validate_symbol(request["symbol"].upper())
    # TODO: check if the same order is in database


def _get_exec_time(date, time):
    return datetime.datetime.combine(
        datetime.datetime.strptime(date, "%Y-%m-%d"),
        datetime.datetime.strptime(time, "%H:%M").time(),
    )
