from src.db.utils import get_cursor

# SQL Order commands
UPDATE_POSITION = """UPDATE position SET
    quantity = %s,
    state = %s
    WHERE id = %s;"""
SELECT_POSITION = """SELECT
    symbol,
    source,
    quantity,
    state,
    portfolio_id,
    id
    FROM position WHERE symbol = %s AND portfolio_id = %s;"""
SELECT_POSITIONS = """SELECT
    symbol,
    source,
    quantity,
    state,
    portfolio_id,
    id
    FROM position WHERE portfolio_id = %s;"""
INSERT_POSITION = """INSERT INTO position (
    symbol,
    source,
    quantity,
    state,
    portfolio_id
    )
    VALUES (%s, %s, %s, %s, %s);"""
DELETE_POSITION = """DELETE FROM Position WHERE id = %s;"""

class DB_Position:

    @staticmethod
    def get_positions(portfolio_id):
        with get_cursor() as cursor:
            cursor.execute(SELECT_POSITIONS, (portfolio_id,))
            return cursor.fetchall()

    @staticmethod
    def get_position(symbol, portfolio_id):
        with get_cursor() as cursor:
            cursor.execute(SELECT_POSITION, (symbol, portfolio_id))
            return cursor.fetchone()

    @staticmethod
    def add_position(symbol, source, quantity, state, port_id):
        with get_cursor() as cursor:
            cursor.execute(INSERT_POSITION, (symbol, source, quantity, state, port_id))

    @staticmethod
    def update_position(quantity, state, position_id):
        with get_cursor() as cursor:
            cursor.execute(UPDATE_POSITION, (quantity, state, position_id))

    @staticmethod
    def delete_position(_id):
        with get_cursor() as cursor:
            cursor.execute(DELETE_POSITION, (_id,))

