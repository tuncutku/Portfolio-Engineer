"""Yahoo market mapping."""

from src.market import Symbol, Currency, Equity, ETF, Index

security_map = {
    "EQUITY": lambda info: Equity(Currency(info["currency"]), Symbol(info["symbol"])),
    "ETF": lambda info: ETF(Currency(info["currency"]), Symbol(info["symbol"])),
    "INDEX": lambda info: Index(Currency(info["currency"]), Symbol(info["symbol"])),
}

currency_map = {
    "USD": Currency("USD"),
    "EUR": Currency("EUR"),
    "CAD": Currency("CAD"),
    "TRY": Currency("TRY"),
}
