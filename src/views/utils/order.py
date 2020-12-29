from typing import List

from src.environment.user_activities import Order


def _extract_open_orders(order_list: List[Order]) -> List[Order]:
    remaining_amount = sum(
        [order.filledQuantity if order.side == "Buy" else order.filledQuantity * -1 for order in order_list]
    )
    open_orders = list()
    for order in reversed(order_list):
        open_orders.append(order)
        remaining_amount = remaining_amount - order.filledQuantity
        if remaining_amount == 0:
            break
    return open_orders
