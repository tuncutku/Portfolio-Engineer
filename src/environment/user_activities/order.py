from pydantic.dataclasses import dataclass
from datetime import datetime
from typing import List

from src.extensions import db
from src.environment.user_activities.base import BaseModel


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
    Cash = "Cash"
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
class Order(BaseModel):
    __tablename__ = "orders"

    id = db.Column(db.Integer(), primary_key=True)
    position_id = db.Column(
        db.Integer(),
        db.ForeignKey("positions.id"),
    )
    symbol = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer(), nullable=False)
    side = db.Column(db.String(255), nullable=False)
    avg_exec_price = db.Column(db.Float(), nullable=False)
    exec_time = db.Column(db.DateTime, nullable=False)
    fee = db.Column(db.Float(), nullable=False)
    # strategyType: str  # ex:"SingleLeg"
    # fee: int = 0

    def __repr__(self):
        return "<Order {}.>".format(self.symbol)

    @property
    def adjusted_quantity(self):
        return self.quantity if self.side == OrderSideType.Buy else (-1) * self.quantity

    def to_dict(self):
        return {
            "ID": self.id,
            "symbol": self.symbol,
            "quantity": self.quantity,
            "side": self.side,
            "avg_exec_price": self.avg_exec_price,
            "exec_time": self.exec_time.strftime("%y-%m-%d %a %H:%M"),
            "fee": self.fee,
        }

    def edit(self, symbol, quantity, side, avg_exec_price, exec_time, fee) -> None:
        self.symbol = symbol
        self.quantity = quantity
        self.side = side
        self.avg_exec_price = avg_exec_price
        self.exec_time = exec_time
        self.fee = fee
        db.session.commit()