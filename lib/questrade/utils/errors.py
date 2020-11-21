# TODO add error handling for Questrade
class QtradeError(Exception):
    def __init__(self, message):
        self.message = message

# WiP
class UserNotFoundError(QtradeError):
    pass

# WiP
class IncorrectPasswordError(QtradeError):
    pass