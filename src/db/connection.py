from contextlib import contextmanager
from psycopg2.extras import DictCursor
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
database_uri = os.environ["DATABASE_URI"]
# connection = psycopg2.connect(database_uri)

connection = psycopg2.connect(
    dbname = "hello_flask_dev",
    user = "postgres",
    host = "db",
    password = "postgres",
)

@contextmanager
def get_cursor():
    with connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            yield cursor