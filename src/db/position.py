from src.db.utils import get_cursor

# SQL Order commands
CREATE_ORDER = ""
INSERT_ORDER = ""
UPDATE_ORDER = ""
DELETE_ORDER = ""

class DB_Position:
    def add_position(email, password):
        with get_cursor() as cursor:
            cursor.execute(INSERT_USER, (email, password))
