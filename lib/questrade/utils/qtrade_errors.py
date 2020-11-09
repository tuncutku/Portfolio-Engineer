class QtradeError(Exception):
    def __init__(self, message):
        self.message = message

# WiP
class UserNotFoundError(QtradeError):
    pass

# WiP
class UserAlreadyRegisteredError(QtradeError):
    pass

# WiP
class InvalidEmailError(QtradeError):
    pass

# WiP
class IncorrectPasswordError(QtradeError):
    pass