from src.db.utils import get_cursor, encrypt_token, decrypt_token

# SQL Questrade Token commands
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


class DB_Token:

    @staticmethod
    def add_user_token(access_token, api_server, expires_at, refresh_token, token_type, email):
        access_token = encrypt_token(access_token)
        refresh_token = encrypt_token(refresh_token)
        with get_cursor() as cursor:
            cursor.execute(INSERT_TOKEN, (access_token, api_server, expires_at, refresh_token, token_type, email))

    @staticmethod
    def update_user_token(access_token, api_server, expires_at, refresh_token, token_type, email):
        access_token = encrypt_token(access_token)
        refresh_token = encrypt_token(refresh_token)
        with get_cursor() as cursor:
            cursor.execute(UPDATE_TOKEN, (access_token, api_server, expires_at, refresh_token, token_type, email))

    @staticmethod
    def find_token_by_user_email(email):
        with get_cursor() as cursor:
            cursor.execute(SELECT_TOKEN_BY_USER_EMAIL, (email,))
            token = cursor.fetchone()
            if token is not None:
                token["access_token"] = decrypt_token(token["access_token"])
                token["refresh_token"] = decrypt_token(token["refresh_token"])
            return token

