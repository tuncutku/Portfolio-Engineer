class UserLevelError(Exception):
    def __init__(self, message):
        self.message = message


class InvalidOrderFeeError(UserLevelError):
    pass


class InvalidOrderAmountError(UserLevelError):
    pass


class InvalidOrderDateError(UserLevelError):
    pass