from typing import List, Tuple
from contextlib import contextmanager

from src.db.connection import get_cursor

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
    id SERIAL PRIMARY KEY
);"""
INSERT_TOKEN = """INSERT INTO user_token (
    access_token,
    api_server,
    expires_at,
    refresh_token,
    token_type,
    email
    )
    VALUES (%s, %s, %s, %s, %s, %s);"""
UPDATE_TOKEN = """UPDATE user_token SET (
    access_token = %s,
    api_server = %s,
    expires_at = %s,
    refresh_token = %s,
    token_type = %s,
    )
    WHERE email = %s;"""
SELECT_TOKEN_BY_USER_EMAIL = """SELECT 
    access_token,
    api_server,
    expires_at,
    refresh_token,
    token_type
    FROM user_token WHERE email = %s;"""

# SQL Portfolio commands
CREATE_PORTFOLIO = ""
INSERT_PORTFOLIO = ""


def create_tables():
    with get_cursor() as cursor:
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_USER_TOKEN)

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
    with get_cursor() as cursor:
        cursor.execute(INSERT_TOKEN, (access_token, api_server, expires_at, refresh_token, token_type, email))

def update_user_token(access_token, api_server, expires_at, refresh_token, token_type, email):
    with get_cursor() as cursor:
        cursor.execute(UPDATE_TOKEN, (access_token, api_server, expires_at, refresh_token, token_type, email))

def find_token_by_user_email(email):
    with get_cursor() as cursor:
        cursor.execute(SELECT_TOKEN_BY_USER_EMAIL, (email,))
        return cursor.fetchone()

# -- portfolios --

