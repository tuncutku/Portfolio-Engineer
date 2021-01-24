from src.questrade import Questrade_Market_Data
from src.views.utils.common import get_quote_from_symbol


def _extend_position_list_with_md(
    market_data_provider: Questrade_Market_Data, position_list: list
) -> list:

    quotes_list = list()
    mkt_cap_list = list()
    for position in position_list:
        quote = get_quote_from_symbol(position.symbol, market_data_provider)
        if quote is not None:
            mkt_cap = quote * position.quantity
        else:
            quote = "Invalid"
            mkt_cap = "Invalid"
        quotes_list.append(quote)
        mkt_cap_list.append(mkt_cap)
    return list(zip(position_list, quotes_list, mkt_cap_list))
