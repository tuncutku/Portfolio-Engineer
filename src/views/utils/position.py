from src.questrade import Questrade_Market_Data


def _extend_position_list(
    market_data_provider: Questrade_Market_Data, position_list: list
) -> list:

    quotes_list = list()
    mkt_cap_list = list()
    for position in position_list:
        raw_symbols = market_data_provider.symbols_search(prefix=position.symbol)
        symbol_id = market_data_provider.get_symbol_id(raw_symbols, position.symbol)
        raw_quote = market_data_provider.markets_quote(id=symbol_id)

        # TODO: Add currency, security type and brief description to the position list.
        quote = raw_quote["quotes"][0]["lastTradePrice"]
        if quote is not None:
            mkt_cap = quote * position.quantity
        else:
            quote = "Invalid"
            mkt_cap = "Invalid"

        quotes_list.append(quote)
        mkt_cap_list.append(mkt_cap)
    return list(zip(position_list, quotes_list, mkt_cap_list))
