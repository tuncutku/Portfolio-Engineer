from src.db.utils import get_cursor

# SQL Portfolio commands
INSERT_PORTFOLIO = """INSERT INTO portfolio (
    name,
    source,
    status,
    type,
    email,
    questrade_id
    )
    VALUES (%s, %s, %s, %s, %s, %s);"""
UPDATE_PORTFOLIO = """UPDATE portfolio SET
    name = %s,
    status = %s,
    type = %s
    WHERE name = %s AND email = %s;"""
SELECT_PORTFOLIOS_BY_USER_EMAIL = """SELECT
    name,
    source,
    status,
    type,
    email,
    questrade_id,
    id
    FROM portfolio WHERE email = %s;"""
SELECT_PORTFOLIO = """SELECT
    name,
    source,
    status,
    type,
    email,
    questrade_id,
    id
    FROM portfolio WHERE name = %s AND email = %s;"""
DELETE_PORTFOLIO = """DELETE FROM portfolio WHERE id = %s;"""

class DB_Portfolio:

    @staticmethod
    def get_portfolio_list(email):
        with get_cursor() as cursor:
            cursor.execute(SELECT_PORTFOLIOS_BY_USER_EMAIL, (email,))
            return cursor.fetchall()

    @staticmethod
    def get_portfolio(name, email):
        with get_cursor() as cursor:
            cursor.execute(SELECT_PORTFOLIO, (name, email))
            return cursor.fetchone()

    @staticmethod
    def add_portfolio(name, source, status, portfolio_type, email, questrade_id = None):
        with get_cursor() as cursor:
            cursor.execute(INSERT_PORTFOLIO, (name, source, status, portfolio_type, email, questrade_id))

    @staticmethod
    def update_portfolio(name, status, portfolio_type, old_name, email):
        with get_cursor() as cursor:
            cursor.execute(UPDATE_PORTFOLIO, (name, status, portfolio_type, old_name, email))

    @staticmethod
    def delete_portfolio(_id):
        with get_cursor() as cursor:
            cursor.execute(DELETE_PORTFOLIO, (_id,))
