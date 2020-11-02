from typing import List, Tuple
from contextlib import contextmanager

from src.db.connection import get_cursor

# SQL user commands
CREATE_USERS = "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, email TEXT, password TEXT);"
INSERT_USER = "INSERT INTO users (email, password) VALUES (%s, %s);"
SELECT_USER_BY_EMAIL = "SELECT email, password, id FROM users WHERE email = %s;"
SELECT_USER_BY_ID = "SELECT email, password, id FROM users WHERE id = %s;"

def create_tables():
    with get_cursor() as cursor:
        cursor.execute(CREATE_USERS)

# -- users --
def add_user(email, password):
    with get_cursor() as cursor:
        cursor.execute(INSERT_USER, (email, password))


def find_user_by_email(email):
    with get_cursor() as cursor:
        cursor.execute(SELECT_USER_BY_EMAIL, (email,))
        return cursor.fetchone()


def find_user_by_id(_id):
    with get_cursor() as cursor:
        cursor.execute(SELECT_USER_BY_ID, (_id,))
        return cursor.fetchone()

# -- portfolios --