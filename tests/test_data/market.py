"""Sample market data"""

from datetime import date
from pandas import Series
from src.market import SingleValue, IndexValue
from src.market.ref_data import cad_ccy, usd_ccy, aapl, up
from src.market.signal import (
    PriceSignal,
    DailyReturnSignal,
    LimitReturnSignal,
)

from tests.test_data.raw_data.fx import fx_index
from tests.test_data.raw_data import security

# Sample market signals
price_signal = PriceSignal(aapl, up, 100)
return_signal = DailyReturnSignal(aapl, up, 0.1)
limit_signal = LimitReturnSignal(aapl, up, 0.1, date(2021, 1, 4))

# Sample series
aapl_series = Series(security.aapl_raw, name="AAPL")
aapl_series_cad = Series(security.aapl_raw_cad, name="AAPL")
aapl_series_round = Series(security.aapl_raw_round, name="AAPL")
aapl_replaced_series = Series(security.aapl_raw_replaced)
appl_mkt_value_series = Series(security.aapl_raw_mkt_value)
appl_pbw_sum_series = Series(security.appl_pbw_sum_raw)
tsla_series = Series(security.tsla_raw, name="TSLA")
pbw_series = Series(security.pbw_raw, name="PBW")
ry_to_series = Series(security.ry_to_raw, name="RY.TO")
gspc_series = Series(security.gspc_raw, name="^GSPC")
usdcad_series = Series(fx_index, name="USDCAD")

# Sample single value
aapl_single_value = SingleValue(aapl_series[-1], usd_ccy)
tsla_single_value = SingleValue(tsla_series[-1], usd_ccy)
ry_to_single_value = SingleValue(ry_to_series[-1], cad_ccy)

# Sample index value
aapl_index = IndexValue(aapl_series, usd_ccy)
tsla_index = IndexValue(tsla_series, usd_ccy)
pbw_index = IndexValue(pbw_series, usd_ccy)
ry_to_index = IndexValue(ry_to_series, cad_ccy)
gspc_index = IndexValue(gspc_series, usd_ccy)
appl_pbw_sum_index = IndexValue(appl_pbw_sum_series, usd_ccy)
appl_mkt_value_index = IndexValue(appl_mkt_value_series, usd_ccy)
aapl_replaced_index = IndexValue(aapl_replaced_series, usd_ccy)
