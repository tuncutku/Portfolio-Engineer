from pydantic.dataclasses import dataclass
from typing import Union
import pandas as pd
import yfinance as yf

security_type_map = {}


class Position:
    def __init__(self, symbol, name, security_type, currency, quantity, market_cap):
        self.symbol = symbol
        self.name = name
        self.security_type = security_type
        self.currency = currency
        self.quantity = quantity
        self.market_cap = market_cap

    def orders(self, orders):
        pass

    @property
    def open(self) -> bool:
        return True if self.quantity != 0 else False

    def generate_trades(self, orders):
        pass

    @classmethod
    def from_df(cls, symbol: str, df: pd.DataFrame):
        symbol_info = yf.Ticker(symbol).info

        quote = (
            yf.Ticker(symbol)
            .history(period="1m", interval="1m")["Close"]
            .values.tolist()
        )
        total_pos_quantity = df["Side amount"].sum()
        mkt_cap = round(quote[0] * total_pos_quantity, 2) if quote else None

        return cls(
            symbol,
            symbol_info.get("shortName", None),
            symbol_info.get("quoteType", None),
            symbol_info.get("currency", None),
            total_pos_quantity,
            mkt_cap,
        )

    @staticmethod
    def position_attributes_map():
        return {
            "Name": "name",
            "Currency": "currency",
            "Market Cap": "market_cap",
        }
