from datetime import datetime
import pandas as pd

from src.tests.utils.base import BaseTest
from src.market_data.yahoo import YFinance


class MarketDataProviderTest(BaseTest):
    def test_yfinance(self):
        """Test for Yfinance wrapper and connection."""

        # Test a Stock and an ETF.
        # TODO: add option coverage.
        securities = ["AAPL", "PBW"]
        quotes = [73.61084, 34.4514]
        md_provider = YFinance(securities)

        self.assertTrue(md_provider.is_valid)
        self.assertIsInstance(md_provider.info(), dict)
        self.assertIsInstance(md_provider.get_current_quotes(), pd.DataFrame)

        pd_raw = md_provider.get_historical_quotes(datetime(2020, 1, 1, 4, 40))
        pd_quote = pd_raw["AAPL"].loc[pd.DatetimeIndex(["2020-01-02"])]
        self.assertEqual(float(pd_quote), 74.33351)

        # Test invalid symbol.
        md_provider = YFinance(["XYZ123456789"])
        self.assertFalse(md_provider.is_valid)
        with self.assertRaises(ValueError):
            md_provider.info()
