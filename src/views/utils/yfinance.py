"""Yahoo market mapping."""

from src.market import Currency, Equity, ETF, Index, Info
from src.market import ref_data

security_map = {
    "EQUITY": lambda symbol: Equity(Currency(symbol.get_info(Info.currency)), symbol),
    "ETF": lambda symbol: ETF(Currency(symbol.get_info(Info.currency)), symbol),
    "INDEX": lambda symbol: Index(Currency(symbol.get_info(Info.currency)), symbol),
}

currency_map = {
    "USD": ref_data.usd_ccy,
    "EUR": ref_data.eur_ccy,
    "CAD": ref_data.cad_ccy,
    "TRY": ref_data.try_ccy,
}
