class TokenError(Exception):
    def __init__(self, message):
        self.message = message

class TokenNotFoundError(TokenError):
    pass

class WrongTokenError(TokenError):
    pass

class InternalServerError(TokenError):
    pass