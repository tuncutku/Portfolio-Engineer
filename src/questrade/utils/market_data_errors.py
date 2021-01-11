class MarketDataError(Exception):
    def __init__(self, message):
        self.message = message

class InvalidSymbolError(MarketDataError):
    pass