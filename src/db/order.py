from src.db.utils import get_cursor

# SQL Order commands
SELECT_ORDERS = """SELECT
    symbol,
    state,
    quantity,
    side,
    average_price,
    time,
    strategy,
    fee,
    portfolio_id,
    position_id,
    id
    FROM orders WHERE position_id = %s;"""
INSERT_ORDER = ""
UPDATE_ORDER = ""
DELETE_ORDER = ""

class DB_Order:
    def get_orders(position_id):
        with get_cursor() as cursor:
            cursor.execute(SELECT_ORDERS, (position_id,))
            return cursor.fetchall()
