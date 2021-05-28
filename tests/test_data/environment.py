"""Sample data for tests"""

from datetime import datetime
import pytz
from pandas import Series, DataFrame

from src.market import IndexValue
from src.market.ref_data import aapl, ry_to, usd_ccy, cad_ccy
from src.market.types import OrderSideType

from tests.test_data.raw_data.quantity import (
    sample_quantity_raw,
    position_1_quantity_raw,
    position_1_cum_quantity_raw,
)
from tests.test_data.raw_data.cost import sample_cost_raw, position_1_cost_raw
from tests.test_data.raw_data.position import (
    position_1_values_raw,
    position_1_values_cad_raw,
)
from tests.test_data.raw_data.portfolio import (
    portfolio_values_raw,
    portfolio_values_usd_raw,
    portfolio_position_values_raw,
    portfolio_position_values_cad_raw,
    portfolio_quantities_raw,
)

sample_quantity = Series(sample_quantity_raw, name="Quantity")
position_1_quantity = Series(position_1_quantity_raw, name="Quantity")
position_1_cum_quantity = Series(position_1_cum_quantity_raw, name="Quantity")

sample_cost = Series(sample_cost_raw, name="Cost")
position_1_cost = Series(position_1_cost_raw, name="Cost")

position_1_values_series = Series(position_1_values_raw)
position_1_values_cad_series = Series(position_1_values_cad_raw)
position_1_values_index = IndexValue(position_1_values_series, usd_ccy)
position_1_values_cad_index = IndexValue(position_1_values_cad_series, cad_ccy)

portfolio_values_series = Series(portfolio_values_raw, name="Portfolio_1")
portfolio_values_usd_series = Series(portfolio_values_usd_raw, name="Portfolio_1")
portfolio_position_values_df = DataFrame(portfolio_position_values_raw)
portfolio_position_values_cad_df = DataFrame(portfolio_position_values_cad_raw)
portfolio_values_index = IndexValue(portfolio_values_series, cad_ccy)
portfolio_values_usd_index = IndexValue(portfolio_values_usd_series, usd_ccy)
portfolio_quantities_df = DataFrame(portfolio_quantities_raw)


# Raw data
order_1_raw = {
    "quantity": 10,
    "direction": OrderSideType.Buy,
    "cost": 130,
    "time": datetime(2020, 2, 3, tzinfo=pytz.utc),
}
order_2_raw = {
    "quantity": 2,
    "direction": OrderSideType.Sell,
    "cost": 122,
    "time": datetime(2020, 7, 1, tzinfo=pytz.utc),
}
order_3_raw = {
    "quantity": 14,
    "direction": OrderSideType.Buy,
    "cost": 126,
    "time": datetime(2021, 1, 13, tzinfo=pytz.utc),
}
order_4_raw = {
    "quantity": 20,
    "direction": OrderSideType.Buy,
    "cost": 100,
    "time": datetime(2019, 11, 13, tzinfo=pytz.utc),
}
order_5_raw = {
    "quantity": 10,
    "direction": OrderSideType.Buy,
    "cost": 111,
    "time": datetime(2020, 7, 1, tzinfo=pytz.utc),
}
order_6_raw = {
    "quantity": 22,
    "direction": OrderSideType.Sell,
    "cost": 115,
    "time": datetime(2020, 9, 10, tzinfo=pytz.utc),
}
position_1_raw = {"security": aapl}
position_2_raw = {"security": ry_to}
portfolio_1_raw = {"name": "portfolio_1"}
user_1_raw = {"email": "tuncutku10@gmail.com", "password": "1234"}
