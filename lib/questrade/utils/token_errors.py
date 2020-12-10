class TokenError(Exception):
    def __init__(self, message):
        self.message = message

class TokenNotFoundError(TokenError):
    pass

class InvalidTokenError(TokenError):
    pass

class InternalServerError(TokenError):
    pass