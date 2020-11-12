from contextlib import contextmanager
from psycopg2.extras import DictCursor
import os
import psycopg2


database_uri = os.environ["DATABASE_URI"]
connection = psycopg2.connect(database_uri)


@contextmanager
def get_cursor():
    with connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            yield cursor