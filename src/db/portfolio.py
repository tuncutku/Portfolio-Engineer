from src.db.utils import get_cursor

# SQL Portfolio commands
CREATE_PORTFOLIO = """CREATE TABLE IF NOT EXISTS portfolio (
    name TEXT,
    source TEXT,
    status TEXT,
    type TEXT,
    email TEXT,
    questrade_id INT,
    FOREIGN KEY (email) REFERENCES users (email),
    id SERIAL PRIMARY KEY);"""
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
    status = %s,
    type = %s
    WHERE name = %s;"""
SELECT_PORTFOLIOS_BY_USER_EMAIL = """SELECT
    name,
    source,
    status,
    type,
    email,
    id,
    questrade_id
    FROM portfolio WHERE email = %s;"""
SELECT_PORTFOLIO = """SELECT
    name,
    source,
    status,
    type,
    email,
    id,
    questrade_id
    FROM portfolio WHERE email = %s AND name = %s;"""

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
    def add_portfolio(name, source, status, portfolio_type, email, questrade_id) -> None:
        with get_cursor() as cursor:
            cursor.execute(INSERT_PORTFOLIO, (name, source, status, portfolio_type, email, questrade_id))

    @staticmethod
    def update_portfolio(status, portfolio_type, name):
        with get_cursor() as cursor:
            cursor.execute(UPDATE_PORTFOLIO, (status, portfolio_type, name))

    @staticmethod
    def update_portfolio_name():
        pass

    @staticmethod
    def delete_portfolio(_id):
        pass
