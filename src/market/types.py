"""Market data types"""

# pylint: disable=too-few-public-methods, invalid-name


from dataclasses import dataclass


# class Format:
#     """Base class for formats."""


# class fmt_d(Format):
#     "${:,.0f}".format("n")


# class fmt_pct(Format):
#     "{0:.2f}%".format("n * 100")


@dataclass
class Direction:
    """Form direction object."""

    direction: str
    n: int


class Exchange:
    """List of exchanges."""

    XNYS = "XNYS"
    XTSE = "XTSE"
    XIST = "XIST"
    EUREX = "EUREX"


class OrderSideType:
    """List of order types."""

    Buy = "Buy"
    Sell = "Sell"
    Short = "Sell Short"
    Cov = "Cover the short"
    BTO = "Buy-to-Open"
    STC = "Sell-to-Close"
    STO = "Sell-to-Open"
    BTC = "Buy-to-Close"


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


class SecurityType:
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


YFinanceSecurityTypeMapping = {
    "EQUITY": SecurityType.Equity,
    "ETF": SecurityType.ETF,
    "OPTION": SecurityType.Option,
}
