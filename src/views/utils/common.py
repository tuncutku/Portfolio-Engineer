from src.questrade import Questrade_Market_Data


def get_quote_from_symbol(symbol: str, md_provider: Questrade_Market_Data):
    raw_symbols = md_provider.symbols_search(prefix=symbol)
    symbol_id = md_provider.get_symbol_id(raw_symbols, symbol)
    raw_quote = md_provider.markets_quote(id=symbol_id)
    # TODO: Add currency, security type and brief description to the position list.
    # TODO: Add market data classes
    return raw_quote["quotes"][0]["lastTradePrice"]
