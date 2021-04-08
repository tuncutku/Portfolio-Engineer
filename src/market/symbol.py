"""Symbol to retrieve market data."""

from functools import partial, cached_property
from pandas_datareader.data import DataReader
from yfinance import Ticker
from pydantic import BaseModel
from datetime import date

from pandas import DataFrame


provider = partial(DataReader, data_source="yahoo")


class Symbol(BaseModel):
    symbol: str

    @cached_property
    def info(self) -> dict:
        return Ticker(self.symbol).info

    @property
    def is_valid(self) -> bool:
        """Valide if the ticker exist in the database source."""
        return bool(self.info.get("symbol"))

    def index(self, start: date, end: date) -> DataFrame:
        return provider(name=self.symbol, start=start, end=end)