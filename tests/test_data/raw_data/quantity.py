"""Sample quantity"""

from pandas import Timestamp

sample_quantity_raw = {
    Timestamp("2020-05-01 00:00:00", freq="B"): 10,
    Timestamp("2020-05-04 00:00:00", freq="B"): 1,
    Timestamp("2020-05-05 00:00:00", freq="B"): 1,
    Timestamp("2020-05-06 00:00:00", freq="B"): 1,
    Timestamp("2020-05-07 00:00:00", freq="B"): 1,
    Timestamp("2020-05-11 00:00:00", freq="B"): 1,
    Timestamp("2020-05-12 00:00:00", freq="B"): 1,
    Timestamp("2020-05-13 00:00:00", freq="B"): 2,
    Timestamp("2020-05-14 00:00:00", freq="B"): 2,
    Timestamp("2020-05-15 00:00:00", freq="B"): 2,
    Timestamp("2020-05-19 00:00:00", freq="B"): 2,
    Timestamp("2020-05-20 00:00:00", freq="B"): 2,
    Timestamp("2020-05-21 00:00:00", freq="B"): 2,
    Timestamp("2020-05-22 00:00:00", freq="B"): 2,
    Timestamp("2020-05-25 00:00:00", freq="B"): 30,
    Timestamp("2020-05-26 00:00:00", freq="B"): 30,
    Timestamp("2020-05-27 00:00:00", freq="B"): 30,
    Timestamp("2020-05-28 00:00:00", freq="B"): 30,
}

position_1_quantity_raw = {
    Timestamp("2020-02-03 00:00:00"): 10,
    Timestamp("2020-07-01 00:00:00"): -2,
    Timestamp("2021-01-13 00:00:00"): 14,
}

position_1_cum_quantity_raw = {
    Timestamp("2020-02-03 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-04 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-05 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-06 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-07 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-10 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-11 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-12 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-13 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-14 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-17 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-18 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-19 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-20 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-21 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-24 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-25 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-26 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-27 00:00:00", freq="B"): 10.0,
    Timestamp("2020-02-28 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-02 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-03 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-04 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-05 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-06 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-09 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-10 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-11 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-12 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-13 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-16 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-17 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-18 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-19 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-20 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-23 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-24 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-25 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-26 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-27 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-30 00:00:00", freq="B"): 10.0,
    Timestamp("2020-03-31 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-01 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-02 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-03 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-06 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-07 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-08 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-09 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-10 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-13 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-14 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-15 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-16 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-17 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-20 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-21 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-22 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-23 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-24 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-27 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-28 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-29 00:00:00", freq="B"): 10.0,
    Timestamp("2020-04-30 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-01 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-04 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-05 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-06 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-07 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-08 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-11 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-12 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-13 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-14 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-15 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-18 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-19 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-20 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-21 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-22 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-25 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-26 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-27 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-28 00:00:00", freq="B"): 10.0,
    Timestamp("2020-05-29 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-01 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-02 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-03 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-04 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-05 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-08 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-09 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-10 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-11 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-12 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-15 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-16 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-17 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-18 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-19 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-22 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-23 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-24 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-25 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-26 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-29 00:00:00", freq="B"): 10.0,
    Timestamp("2020-06-30 00:00:00", freq="B"): 10.0,
    Timestamp("2020-07-01 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-02 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-03 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-06 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-07 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-08 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-09 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-10 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-13 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-14 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-15 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-16 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-17 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-20 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-21 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-22 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-23 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-24 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-27 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-28 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-29 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-30 00:00:00", freq="B"): 8.0,
    Timestamp("2020-07-31 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-03 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-04 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-05 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-06 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-07 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-10 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-11 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-12 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-13 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-14 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-17 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-18 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-19 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-20 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-21 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-24 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-25 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-26 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-27 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-28 00:00:00", freq="B"): 8.0,
    Timestamp("2020-08-31 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-01 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-02 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-03 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-04 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-07 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-08 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-09 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-10 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-11 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-14 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-15 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-16 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-17 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-18 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-21 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-22 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-23 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-24 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-25 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-28 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-29 00:00:00", freq="B"): 8.0,
    Timestamp("2020-09-30 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-01 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-02 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-05 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-06 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-07 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-08 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-09 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-12 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-13 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-14 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-15 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-16 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-19 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-20 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-21 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-22 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-23 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-26 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-27 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-28 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-29 00:00:00", freq="B"): 8.0,
    Timestamp("2020-10-30 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-02 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-03 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-04 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-05 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-06 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-09 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-10 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-11 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-12 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-13 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-16 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-17 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-18 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-19 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-20 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-23 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-24 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-25 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-26 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-27 00:00:00", freq="B"): 8.0,
    Timestamp("2020-11-30 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-01 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-02 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-03 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-04 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-07 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-08 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-09 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-10 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-11 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-14 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-15 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-16 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-17 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-18 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-21 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-22 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-23 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-24 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-25 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-28 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-29 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-30 00:00:00", freq="B"): 8.0,
    Timestamp("2020-12-31 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-01 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-04 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-05 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-06 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-07 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-08 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-11 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-12 00:00:00", freq="B"): 8.0,
    Timestamp("2021-01-13 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-14 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-15 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-18 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-19 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-20 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-21 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-22 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-25 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-26 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-27 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-28 00:00:00", freq="B"): 22.0,
    Timestamp("2021-01-29 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-01 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-02 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-03 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-04 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-05 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-08 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-09 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-10 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-11 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-12 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-15 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-16 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-17 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-18 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-19 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-22 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-23 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-24 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-25 00:00:00", freq="B"): 22.0,
    Timestamp("2021-02-26 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-01 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-02 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-03 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-04 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-05 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-08 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-09 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-10 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-11 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-12 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-15 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-16 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-17 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-18 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-19 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-22 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-23 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-24 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-25 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-26 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-29 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-30 00:00:00", freq="B"): 22.0,
    Timestamp("2021-03-31 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-01 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-02 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-05 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-06 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-07 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-08 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-09 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-12 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-13 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-14 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-15 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-16 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-19 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-20 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-21 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-22 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-23 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-26 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-27 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-28 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-29 00:00:00", freq="B"): 22.0,
    Timestamp("2021-04-30 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-03 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-04 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-05 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-06 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-07 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-10 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-11 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-12 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-13 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-14 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-17 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-18 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-19 00:00:00", freq="B"): 22.0,
    Timestamp("2021-05-20 00:00:00", freq="B"): 22.0,
}