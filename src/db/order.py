from src.db.utils import get_cursor

# SQL Order commands
SELECT_ORDERS = """SELECT
    symbol,
    source,
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
INSERT_ORDER = """INSERT INTO orders (
    symbol,
    source,
    state,
    quantity,
    side,
    average_price,
    time,
    strategy,
    fee,
    portfolio_id,
    position_id
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
UPDATE_ORDER = ""
DELETE_ORDER = ""

class DB_Order:
    
    @staticmethod
    def get_orders(position_id):
        with get_cursor() as cursor:
            cursor.execute(SELECT_ORDERS, (position_id,))
            return cursor.fetchall()
    
    @staticmethod
    def add_order(        
        symbol,
        source,
        state,
        filledQuantity,
        side,
        avg_exec_price,
        exec_time,
        strategyType,
        portfolio_id,
        fee,
        position_id,
    ):
        with get_cursor() as cursor:
            cursor.execute(INSERT_ORDER, (
                symbol,
                source,
                state,
                filledQuantity,
                side,
                avg_exec_price,
                exec_time,
                strategyType,
                portfolio_id,
                fee,
                position_id,
                )
            )