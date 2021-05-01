from src.market import Currency, Equity, ETF, Index

security_map = {
    "EQUITY": lambda info: Equity(
        asset_currency=info["currency"], symbol=info["symbol"]
    ),
    "ETF": lambda info: ETF(asset_currency=info["currency"], symbol=info["symbol"]),
    "INDEX": lambda info: Index(asset_currency=info["currency"], symbol=info["symbol"]),
}
