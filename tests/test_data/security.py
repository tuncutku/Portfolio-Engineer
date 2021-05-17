"""Sample ETF"""

from pandas import Timestamp

pbw = {
    Timestamp("2020-01-06 00:00:00"): 34.660030364990234,
    Timestamp("2020-01-07 00:00:00"): 34.719417572021484,
    Timestamp("2020-01-08 00:00:00"): 34.96684265136719,
    Timestamp("2020-01-09 00:00:00"): 35.27365493774414,
    Timestamp("2020-01-10 00:00:00"): 35.28355407714844,
    Timestamp("2020-01-13 00:00:00"): 36.30297088623047,
    Timestamp("2020-01-14 00:00:00"): 36.76813888549805,
    Timestamp("2020-01-15 00:00:00"): 36.906700134277344,
    Timestamp("2020-01-16 00:00:00"): 37.30258560180664,
    Timestamp("2020-01-17 00:00:00"): 37.62919235229492,
    Timestamp("2020-01-21 00:00:00"): 37.81724548339844,
    Timestamp("2020-01-22 00:00:00"): 37.144229888916016,
    Timestamp("2020-01-23 00:00:00"): 37.22340774536133,
}

pbw_daily_cum_return = {
    Timestamp("2020-01-07 00:00:00"): 1.0017134205136542,
    Timestamp("2020-01-08 00:00:00"): 1.0088520489782047,
    Timestamp("2020-01-09 00:00:00"): 1.0177040979564094,
    Timestamp("2020-01-10 00:00:00"): 1.0179897047288227,
    Timestamp("2020-01-13 00:00:00"): 1.0474015892063313,
    Timestamp("2020-01-14 00:00:00"): 1.0608224660598449,
    Timestamp("2020-01-15 00:00:00"): 1.0648201904507404,
    Timestamp("2020-01-16 00:00:00"): 1.0762421500785997,
    Timestamp("2020-01-17 00:00:00"): 1.085665302541218,
    Timestamp("2020-01-21 00:00:00"): 1.0910909507337674,
    Timestamp("2020-01-22 00:00:00"): 1.0716733222032906,
    Timestamp("2020-01-23 00:00:00"): 1.0739577361409451,
}