class PositionError(Exception):
    def __init__(self, message):
        self.message = message


class PositionNotFoundError(PositionError):
    pass