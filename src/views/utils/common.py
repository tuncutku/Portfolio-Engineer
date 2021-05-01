from src.market import Symbol, Security


def get_security(symbol: Symbol) -> Security:
    """Form security by given symbol."""

    info = symbol.info
    f = security_map[info["quoteType"]]
    return f(info)