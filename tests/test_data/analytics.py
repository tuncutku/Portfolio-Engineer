"""Sample data for analytics tests"""

from pandas import DataFrame, concat

from tests.test_data.market import aapl_series, ry_to_series
from tests.test_data.raw_data.quantity import portfolio_quantities
from tests.test_data.raw_data.analytics import (
    periodic_return_cum_raw,
    periodic_return_raw,
)

periodic_return_df = DataFrame(periodic_return_raw)
periodic_return_cum_df = DataFrame(periodic_return_cum_raw)

securities_df = concat([aapl_series, ry_to_series], axis=1)
quantities_df = DataFrame(portfolio_quantities)
