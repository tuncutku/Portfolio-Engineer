from contextlib import contextmanager
from psycopg2.extras import DictCursor
from psycopg2 import pool
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection_pool(test_case: bool = False):
    url = os.environ["DATABASE_URI_TEST"] if test_case else os.environ["DATABASE_URI"]
    return pool.SimpleConnectionPool(1, 10, dsn=url)


db_pool = get_connection_pool()


@contextmanager
def database_manager():
    connection = db_pool.getconn()
    try:
        with connection:
            with connection.cursor(cursor_factory=DictCursor) as cursor:
                yield cursor
    finally:
        cursor.close()
        db_pool.putconn(connection)


# connection = psycopg2.connect(
#     dbname = "hello_flask_dev",
#     user = "postgres",
#     host = "db",
#     password = "postgres",
# )
