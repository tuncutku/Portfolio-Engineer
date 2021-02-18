from datetime import datetime

from src.tests.utils.base import BaseTest
from src.market_data.yahoo import YFinance


class MarketDataProviderTest(BaseTest):
    def test_yfinance(self):
        """Test for Yfinance wrapper and connection."""

        # Test a Stock and an ETF.
        # TODO: add option coverage.
        securities = ["AAPL", "PBW"]
        quotes = [73.61084, 34.4514]
        for security, quote in zip(securities, quotes):
            md_provider = YFinance(security)
            self.assertEqual(md_provider.symbol, security)
            self.assertTrue(md_provider.is_valid)
            self.assertIsInstance(md_provider.info(), dict)
            self.assertIsInstance(md_provider.get_quote(), float)
            self.assertEqual(
                md_provider.get_historical_quote(datetime(2020, 1, 3)), quote
            )

        # Test invalid symbol.
        md_provider = YFinance("XYZ123456789")
        self.assertFalse(md_provider.is_valid)
        with self.assertRaises(ValueError):
            md_provider.info()
