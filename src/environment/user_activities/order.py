from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import List

from src.db import DB_Order
from src import db_1


class Exchange:
    TSX = "Toronto Stock Exchange"
    TSXV = "Toronto Venture Exchange"
    CNSX = "Canadian National Stock Exchange"
    MX = "Montreal Exchange"
    NASDAQ = "NASDAQ"
    NYSE = "New York Stock Exchange"
    NYSEAM = "NYSE AMERICAN"
    ARCA = "NYSE Arca"
    OPRA = "Option Reporting Authority"
    PinkSheets = "Pink Sheets"
    OTCBB = "OTC Bulletin Board"


class OrderSideType:
    Buy = "Buy"
    Sell = "Sell"
    Short = "Sell Short"
    Cov = "Cover the short"
    BTO = "Buy-to-Open"
    STC = "Sell-to-Close"
    STO = "Sell-to-Open"
    BTC = "Buy-to-Close"


class OptionType:
    Call = "Call"
    Put = "Put"


class OptionDurationType:
    Weekly = "Weekly expiry cycle"
    Monthly = "Monthly expiry cycle"
    Quarterly = "Quarterly expiry cycle"
    LEAP = "Long-term Equity Appreciation contracts"


class OptionExerciseType:
    American = "American option"
    European = "European option"


class OptionStrategyType:
    CoveredCall = "Covered Call"
    MarriedPuts = "Married Put"
    VerticalCallSpread = "Vertical Call"
    VerticalPutSpread = "Vertical Put"
    CalendarCallSpread = "Calendar Call"
    CalendarPutSpread = "Calendar Put"
    DiagonalCallSpread = "Diagonal Call"
    DiagonalPutSpread = "Diagonal Put"
    Collar = "Collar"
    Straddle = "Straddle"
    Strangle = "Strangle"
    ButterflyCall = "Butterfly Call"
    ButterflyPut = "Butterfly Put"
    IronButterfly = "Iron Butterfly"
    CondorCall = "Condor"
    Custom = "Custom"


class SecurityType:
    Stock = "Common and preferred equities, ETFs, ETNs, units, ADRs, etc."
    ETF = "Exchange traded fund"
    Option = "Equity and index options."
    Bond = "Debentures, notes, bonds, both corporate and government."
    Right = "Equity or bond rights and warrants."
    Gold = "Physical gold (coins, wafers, bars)."
    MutualFund = "Canadian or US mutual funds."
    Index = "Stock indices (e.g., Dow Jones)."
    CryptoCurrency = "Crypto currency"


# TODO: Add leg property for multileg options
# TODO: Add currency
class Order(db_1.Model):
    __tablename__ = "orders"

    id = db_1.Column(db_1.Integer(), primary_key=True)
    portfolio_id = db_1.Column(
        db_1.Integer(),
        db_1.ForeignKey("portfolios.id", ondelete="CASCADE"),
        nullable=False,
    )
    symbol = db_1.Column(db_1.String(255), nullable=False)
    quantity = db_1.Column(db_1.Integer(), nullable=False)
    side = db_1.Column(db_1.String(255), nullable=False)
    avg_exec_price = db_1.Column(db_1.Float(), nullable=False)
    exec_time = db_1.Column(db_1.DateTime, nullable=False)
    fee = db_1.Column(db_1.Float(), nullable=False)
    # strategyType: str  # ex:"SingleLeg"
    # fee: int = 0

    def __init__(self, symbol, quantity, side, avg_exec_price, exec_time, fee):
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.avg_exec_price = avg_exec_price
        self.exec_time = exec_time
        self.fee = fee

    def to_dict(self):
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "side": self.side,
            "avg_exec_price": self.avg_exec_price,
            "exec_time": self.exec_time,
            "fee": self.fee,
            "portfolio_id": self.portfolio_id,
        }
