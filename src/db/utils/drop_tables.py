from src.db.utils.connection import get_cursor


DROP_USERS = """DROP TABLE IF EXISTS users;"""
DROP_USER_TOKEN = """DROP TABLE IF EXISTS user_token;"""
DROP_PORTFOLIO = """DROP TABLE IF EXISTS portfolio;"""
DROP_POSITION = """DROP TABLE IF EXISTS position"""
DROP_ORDERS = """DROP TABLE IF EXISTS orderS"""

def drop_tables():
    with get_cursor() as cursor:
        cursor.execute(DROP_ORDERS)
        cursor.execute(DROP_POSITION)
        cursor.execute(DROP_PORTFOLIO)
        cursor.execute(DROP_USER_TOKEN)
        cursor.execute(DROP_USERS)