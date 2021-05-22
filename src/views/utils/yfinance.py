"""Yahoo market mapping."""

from src.market import Symbol, Currency, Equity, ETF, Index
from src.market import ref_data

security_map = {
    "EQUITY": lambda info: Equity(Currency(info["currency"]), Symbol(info["symbol"])),
    "ETF": lambda info: ETF(Currency(info["currency"]), Symbol(info["symbol"])),
    "INDEX": lambda info: Index(Currency(info["currency"]), Symbol(info["symbol"])),
}

currency_map = {
    "USD": ref_data.usd_ccy,
    "EUR": ref_data.eur_ccy,
    "CAD": ref_data.cad_ccy,
    "TRY": ref_data.try_ccy,
}
