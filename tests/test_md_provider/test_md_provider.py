from datetime import datetime
import pandas as pd
import pytest

from src.market_data.provider import YFinance


def test_yfinance():
    """Test for Yfinance wrapper and connection."""

    # Test a Stock and an ETF.
    securities = ["AAPL", "PBW", "ES=F"]
    quotes = [73.61084, 34.4514]
    md_provider = YFinance(securities)

    assert md_provider.is_valid == True
    assert isinstance(md_provider.info(), dict)
    assert isinstance(md_provider.get_current_quotes(), pd.DataFrame)

    pd_raw = md_provider.get_historical_quotes(datetime(2020, 1, 1, 4, 40))
    pd_quote = pd_raw["AAPL"].loc[pd.DatetimeIndex(["2020-01-02"])]
    assert float(pd_quote) == pytest.approx(74.33351, 1)

    # Test invalid symbol.
    md_provider = YFinance(["XYZ123456789GYT"])
    assert md_provider.is_valid == False
