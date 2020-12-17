from src.db.utils import get_cursor

# SQL User commands
INSERT_USER = "INSERT INTO users (email, password) VALUES (%s, %s);"
SELECT_USER_BY_EMAIL = "SELECT email, password FROM users WHERE email = %s;"

class DB_User:

    @staticmethod
    def add_user(email, password):
        with get_cursor() as cursor:
            cursor.execute(INSERT_USER, (email, password))

    @staticmethod
    def find_user_by_email(email):
        with get_cursor() as cursor:
            cursor.execute(SELECT_USER_BY_EMAIL, (email,))
            return cursor.fetchone()

