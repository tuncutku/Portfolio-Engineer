from src.db.utils import get_cursor

# SQL Order commands
SELECT_ORDER = """SELECT
    symbol,
    source,
    state,
    quantity,
    side,
    average_price,
    time,
    strategy,
    portfolio_id,
    fee,
    position_id,
    id
    FROM orders WHERE id = %s;"""
SELECT_ORDERS_BY_POSITION = """SELECT
    symbol,
    source,
    state,
    quantity,
    side,
    average_price,
    time,
    strategy,
    portfolio_id,
    fee,
    position_id,
    id
    FROM orders WHERE position_id = %s;"""
SELECT_ORDERS_BY_SYMBOL = """SELECT
    symbol,
    source,
    state,
    quantity,
    side,
    average_price,
    time,
    strategy,
    portfolio_id,
    fee,
    position_id,
    id
    FROM orders WHERE portfolio_id = %s AND symbol = %s;"""
UPDATE_ORDER = """UPDATE orders SET
    symbol = %s,
    source = %s,
    state = %s,
    quantity = %s,
    side = %s,
    average_price = %s,
    time = %s,
    strategy = %s,
    portfolio_id = %s,
    fee = %s,
    position_id = %s
    WHERE id = %s;"""
UPDATE_ORDER_POSITION_ID = """UPDATE orders SET
    position_id = %s
    WHERE id = %s;"""
INSERT_ORDER = """INSERT INTO orders (
    symbol,
    source,
    state,
    quantity,
    side,
    average_price,
    time,
    strategy,
    portfolio_id,
    fee,
    position_id
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
DELETE_ORDER = """DELETE FROM orders WHERE id = %s;"""


class DB_Order:
    
    @staticmethod
    def get_orders(position_id):
        with get_cursor() as cursor:
            cursor.execute(SELECT_ORDERS_BY_POSITION, (position_id,))
            return cursor.fetchall()

    @staticmethod
    def get_orders_by_symbol(portfolio_id, symbol):
        with get_cursor() as cursor:
            cursor.execute(SELECT_ORDERS_BY_SYMBOL, (portfolio_id, symbol))
            return cursor.fetchall()
    
    @staticmethod
    def get_order(order_id):
        with get_cursor() as cursor:
            cursor.execute(SELECT_ORDER, (order_id,))
            return cursor.fetchone()
    
    @staticmethod
    def delete_order(order_id):
        with get_cursor() as cursor:
            cursor.execute(DELETE_ORDER, (order_id,))

    @staticmethod
    def update_position_id(order_id, position_id):
        with get_cursor() as cursor:
            cursor.execute(UPDATE_ORDER_POSITION_ID, (position_id, order_id))
    
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
        fee,
        portfolio_id,
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

    @staticmethod
    def update_order(        
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
        order_id
    ):
        with get_cursor() as cursor:
            cursor.execute(UPDATE_ORDER, (
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
                order_id,
                )
            )

