"""Market data types"""

# pylint: disable=no-member, invalid-name, too-few-public-methods


from dataclasses import dataclass
from enum import Enum


# class Format:
#     """Base class for formats."""


# class fmt_d(Format):
#     "${:,.0f}".format("n")


# class fmt_pct(Format):
#     "{0:.2f}%".format("n * 100")


@dataclass
class Direction:
    """Form direction object."""

    name: str
    value: int

    def __repr__(self) -> str:
        return self.name.capitalize()

    def __mul__(self, other: float) -> float:
        return self.value * other

    def __rmul__(self, other: float) -> float:
        return self * other


class Period(Enum):
    """Form periods."""

    day = 1
    week = 5
    month = 21
    year = 252


class Sector(Enum):
    """Form sectors with regards to The Global Industry Classification Standard."""

    energy = "Energy"
    materials = "Materials"
    industrials = "Industrials"
    consumer_discretionary = "Consumer discretionary"
    consumer_staples = "Consumer staples"
    healthcare = "Healthcare"
    financials = "Financials"
    information_technology = "Information techonolgy"
    communication_services = "Communication services"
    utilities = "Utilities"
    real_estate = "Real estate"
    other = "other"


class Exchange:
    """List of exchanges."""

    XNYS = "XNYS"
    XTSE = "XTSE"
    XIST = "XIST"
    EUREX = "EUREX"


class OptionType:
    """List of option payoff types."""

    Call = "Call"
    Put = "Put"


class OptionStrategyType:
    """List of option strategy types."""

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


class AlertPeriod:
    """List of alert period durations."""

    TradingDaysEvery5Min = "5m"
    TradingDaysDaily = "1d"


class InstrumentType:
    """List of security types."""

    Cash = "Cash"
    Equity = "Common and preferred equities"
    ETF = "Exchange traded fund"
    Option = "Equity and index options."
    Bond = "Debentures, notes, bonds, both corporate and government."
    Right = "Equity or bond rights and warrants."
    Gold = "Physical gold (coins, wafers, bars)."
    MutualFund = "Canadian or US mutual funds."
    Index = "Stock indices (e.g., Dow Jones)."
    CryptoCurrency = "Crypto currency"


class PortfolioType:
    """List of portfolio types."""

    tfsa = "TFSA"
    rrsp = "RRSP"
    margin = "Margin"
    cash = "Cash"
    custom = "Custom"


YFinanceInstrumentTypeMapping = {
    "EQUITY": InstrumentType.Equity,
    "ETF": InstrumentType.ETF,
    "OPTION": InstrumentType.Option,
}
