class PortfolioError(Exception):
    def __init__(self, message):
        self.message = message


class PortfolioNotFoundError(PortfolioError):
    pass

