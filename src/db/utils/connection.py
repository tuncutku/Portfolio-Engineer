from contextlib import contextmanager
from psycopg2.extras import DictCursor
from psycopg2 import pool
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
database_uri = os.environ["DATABASE_URI"]
connection = psycopg2.connect(database_uri)


db_pool = pool.SimpleConnectionPool(1, 25, dsn=os.environ["DATABASE_URI"])


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
