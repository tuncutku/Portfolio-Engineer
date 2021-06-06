"""Sample cost data"""

from pandas import Timestamp

sample_cost_raw = {
    Timestamp("2020-04-28 00:00:00", freq="B"): 80,
    Timestamp("2020-05-04 00:00:00", freq="B"): 81,
    Timestamp("2020-05-13 00:00:00", freq="B"): 82,
    Timestamp("2020-05-14 00:00:00", freq="B"): 83,
    Timestamp("2020-06-04 00:00:00", freq="B"): 84,
}

position_1_cost_raw = {
    Timestamp("2020-02-03 00:00:00"): 130,
    Timestamp("2020-07-01 00:00:00"): 122,
    Timestamp("2021-01-13 00:00:00"): 126,
}
