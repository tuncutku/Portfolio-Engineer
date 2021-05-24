"""Sample data for tests"""

from pandas import DataFrame

from tests.test_data.raw_data.analytics import (
    periodic_return_cum_raw,
    periodic_return_raw,
)

periodic_return_df = DataFrame(periodic_return_raw)
periodic_return_cum_df = DataFrame(periodic_return_cum_raw)
