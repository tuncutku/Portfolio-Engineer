"""Test indicators"""

from numpy import isnan
from pandas import DataFrame, Series
from src.analytics import indicators
from tests.test_data.raw_data.analytics import indices

from ta import volatility

indices_df = DataFrame(indices)
_high = indices_df["High"]
_low = indices_df["Low"]
_open = indices_df["Open"]
_close = indices_df["Close"]
_volume = indices_df["High"]
_adj_close = indices_df["Adj Close"]


def test_bollinger_bands():
    """Test Bollinger Bands."""

    bands = indicators.bollinger_bands(_close)
    assert isinstance(bands, DataFrame)
    assert bands.shape == (22, 4)
    result = bands.values[~isnan(bands.values)].sum()
    assert round(result, 5) == 500.08004


def test_average_true_range():
    """Test average true range."""

    true_range = indicators.average_true_range(_high, _low, _close)
    assert isinstance(true_range, Series)
    assert true_range.shape == (22,)
    result = true_range.values[~isnan(true_range.values)].sum()
    assert round(result, 5) == 4.36237


def test_keltner_channel():
    """Test keltner channel."""

    keltner_channel = indicators.keltner_channel(_high, _low, _close)
    assert isinstance(keltner_channel, DataFrame)
    assert keltner_channel.shape == (22, 7)
    result = keltner_channel.values[~isnan(keltner_channel.values)].sum()
    assert round(result, 5) == 5143.7484

    keltner_channel_2 = indicators.keltner_channel(_high, _low, _close, original=False)
    assert isinstance(keltner_channel_2, DataFrame)
    assert keltner_channel_2.shape == (22, 7)
    result = keltner_channel_2.values[~isnan(keltner_channel_2.values)].sum()
    assert round(result, 5) == 729.18664
