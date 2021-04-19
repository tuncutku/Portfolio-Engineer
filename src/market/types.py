class Exchange:
    XNYS = "XNYS"
    XTSE = "XTSE"
    XIST = "XIST"
    EUREX = "EUREX"


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


class AlertPeriod:
    TradingDaysEvery5Min = "5m"
    TradingDaysDaily = "1d"


class SecurityType:
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


YFinanceSecurityTypeMapping = {
    "EQUITY": SecurityType.Equity,
    "ETF": SecurityType.ETF,
    "OPTION": SecurityType.Option,
}
