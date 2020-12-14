from typing import List, Tuple
from contextlib import contextmanager

from src.app.db.connection import get_cursor
from src.app.db.encryption import encrypt_token, decrypt_token

# SQL user commands
CREATE_USERS = "CREATE TABLE IF NOT EXISTS users (email TEXT PRIMARY KEY, password TEXT);"
INSERT_USER = "INSERT INTO users (email, password) VALUES (%s, %s);"
SELECT_USER_BY_EMAIL = "SELECT email, password FROM users WHERE email = %s;"

# SQL Questrade Token commands
CREATE_USER_TOKEN = """CREATE TABLE IF NOT EXISTS user_token (
    access_token TEXT,
    api_server TEXT,
    expires_at TEXT,
    refresh_token TEXT,
    token_type TEXT,
    email TEXT,
    FOREIGN KEY (email) REFERENCES users (email),
    id SERIAL PRIMARY KEY);"""
INSERT_TOKEN = """INSERT INTO user_token (
    access_token,
    api_server,
    expires_at,
    refresh_token,
    token_type,
    email
    )
    VALUES (%s, %s, %s, %s, %s, %s);"""
UPDATE_TOKEN = """UPDATE user_token SET
    access_token = %s,
    api_server = %s,
    expires_at = %s,
    refresh_token = %s,
    token_type = %s
    WHERE email = %s;"""
SELECT_TOKEN_BY_USER_EMAIL = """SELECT 
    access_token,
    api_server,
    expires_at,
    refresh_token,
    token_type
    FROM user_token WHERE email = %s;"""

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

# SQL Order commands
CREATE_ORDER = ""
INSERT_ORDER = ""
UPDATE_ORDER = ""
DELETE_ORDER = ""

def create_tables():
    with get_cursor() as cursor:
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_USER_TOKEN)
        cursor.execute(CREATE_PORTFOLIO)

# -- users --
def add_user(email, password):
    with get_cursor() as cursor:
        cursor.execute(INSERT_USER, (email, password))


def find_user_by_email(email):
    with get_cursor() as cursor:
        cursor.execute(SELECT_USER_BY_EMAIL, (email,))
        return cursor.fetchone()

# -- user tokens --
def add_user_token(access_token, api_server, expires_at, refresh_token, token_type, email):
    access_token = encrypt_token(access_token)
    refresh_token = encrypt_token(refresh_token)
    with get_cursor() as cursor:
        cursor.execute(INSERT_TOKEN, (access_token, api_server, expires_at, refresh_token, token_type, email))

def update_user_token(access_token, api_server, expires_at, refresh_token, token_type, email):
    access_token = encrypt_token(access_token)
    refresh_token = encrypt_token(refresh_token)
    with get_cursor() as cursor:
        cursor.execute(UPDATE_TOKEN, (access_token, api_server, expires_at, refresh_token, token_type, email))

def find_token_by_user_email(email):
    with get_cursor() as cursor:
        cursor.execute(SELECT_TOKEN_BY_USER_EMAIL, (email,))
        token = cursor.fetchone()
        if token is not None:
            token["access_token"] = decrypt_token(token["access_token"])
            token["refresh_token"] = decrypt_token(token["refresh_token"])
        return token

# -- portfolios --
def get_portfolio_list(email):
    with get_cursor() as cursor:
        cursor.execute(SELECT_PORTFOLIOS_BY_USER_EMAIL, (email,))
        return cursor.fetchall()

def get_portfolio(name, email):
    with get_cursor() as cursor:
        cursor.execute(SELECT_PORTFOLIO, (name, email))
        return cursor.fetchone()

def add_portfolio(name, source, status, portfolio_type, email, questrade_id) -> None:
    with get_cursor() as cursor:
        cursor.execute(INSERT_PORTFOLIO, (name, source, status, portfolio_type, email, questrade_id))

def update_portfolio(status, portfolio_type, name):
    with get_cursor() as cursor:
        cursor.execute(UPDATE_PORTFOLIO, (status, portfolio_type, name))


def update_portfolio_name():
    pass

def delete_portfolio(_id):
    pass
