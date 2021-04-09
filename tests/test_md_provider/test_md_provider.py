from datetime import datetime, date
import pandas as pd
import pytest

from src.market.provider import YFinance
from src.market.security.etf import ETF
from src.market.symbol import Symbol


def test_hey():

    A = Symbol("PBW")
    etf = ETF(A)

    etf.current_value

    etf.index(date(2019, 1, 10), date.today())

    a = 1


def test_yfinance():
    """Test for Yfinance wrapper and connection."""

    # Test a Stock and an ETF.
    securities = ["AAPL", "PBW", "ES=F"]
    md_provider = YFinance(securities)

    assert md_provider.is_valid is True
    assert isinstance(md_provider.info(), dict)
    assert isinstance(md_provider.get_current_quotes(), pd.DataFrame)

    pd_raw = md_provider.get_historical_quotes(datetime(2020, 1, 1, 4, 40))
    pd_quote = pd_raw["AAPL"].loc[pd.DatetimeIndex(["2020-01-02"])]
    assert float(pd_quote) == pytest.approx(74.33351, 1)

    # Test invalid symbol.
    md_provider = YFinance(["XYZ123456789GYT"])
    assert md_provider.is_valid is False
