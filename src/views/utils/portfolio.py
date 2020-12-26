from typing import List

from src.environment.user_activities.position import Position

def _modify_position_list(positions_questrade: list, positions_db: list):
    """Modify a list of dictionaries so that the keys will be symbols."""

    questrade_positions_dict = {position["symbol"]: position["openQuantity"] for position in positions_questrade}
    db_positions_dict_open = {position.symbol: position.quantity for position in positions_db if position.state == "Open"}
    db_positions_dict_closed = {position.symbol: position.quantity for position in positions_db if position.state == "Closed"}

    return questrade_positions_dict, db_positions_dict_open, db_positions_dict_closed


def _check_position_validity(positions: List[Position]):
    """Check if sum of order amount verifies the position amount."""
    for position in positions:

        a = 1
