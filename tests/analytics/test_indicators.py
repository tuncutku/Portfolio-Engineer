"""Test indicators"""

from typing import Union

import pytest
from numpy import isnan
from pandas import DataFrame, Series
from src.analytics import indicators as ind
from tests.test_data.raw_data.analytics import indices

from ta import volatility

indices_df = DataFrame(indices)
_high = indices_df["High"]
_low = indices_df["Low"]
_open = indices_df["Open"]
_close = indices_df["Close"]
_volume = indices_df["High"]
_adj_close = indices_df["Adj Close"]


volatility_indicators = (
    (ind.bollinger_bands(_close), DataFrame, (22, 4), 500.08004),
    (ind.average_true_range(_high, _low, _close), Series, (22,), 4.36237),
    (ind.keltner_channel(_high, _low, _close), DataFrame, (22, 7), 5143.7484),
    (
        ind.keltner_channel(_high, _low, _close, original=False),
        DataFrame,
        (22, 7),
        729.18664,
    ),
    (ind.donchian_channel(_high, _low, _close), DataFrame, (22, 5), 731.40188),
    (ind.ulcer_index(_close), Series, (22,), 2.83994),
)

momentum_indicators = (
    (ind.relative_strenght_index(_close), Series, (22,), 599.60509),
    (ind.stochastic_oscillator(_high, _low, _close), DataFrame, (22, 2), 599.60509),
    (
        ind.stochastic_oscillator(_high, _low, _close),
        DataFrame,
        (22, 2),
        1304.0419520066328,
    ),
    (ind.kama(_close), Series, (22,), 599.60509),
    (ind.rate_of_change(_close), Series, (22,), 1023.09199),
    (ind.awesome_oscillator(_high, _low), Series, (22,), 1023.09199),
    (ind.williams_r(_high, _low, _close), Series, (22,), 1023.09199),
    (ind.stochastic_rsi(_close), DataFrame, (22, 5), 731.40188),
    (ind.percentage_price_oscillator(_close), DataFrame, (22, 5), 731.40188),
    (ind.percentage_volume_oscillator(_close), DataFrame, (22, 5), 731.40188),
)

volume_indicators = (
    (ind.acc_dist_index(_high, _low, _close, _volume), Series, (22, 4), 500.08004),
    (ind.on_balance_volume(_close, _volume), Series, (22, 4), 500.08004),
    (ind.chaikin_money_flow(_high, _low, _close, _volume), Series, (22, 4), 500.08004),
    (ind.force_index(_close, _volume), Series, (22, 4), 500.08004),
    (ind.ease_of_movement(_high, _low, _volume), DataFrame, (22, 4), 500.08004),
    (ind.volume_price_trend(_close, _volume), Series, (22, 4), 500.08004),
    (ind.negative_volume_index(_close, _volume), Series, (22, 4), 500.08004),
    (ind.money_flow_index(_high, _low, _close, _volume), Series, (22, 4), 500.08004),
    (
        ind.volume_weighted_average_price(_high, _low, _close, _volume),
        Series,
        (22, 4),
        500.08004,
    ),
)


@pytest.mark.parametrize("func, pandas_type, dim, sum_result", volatility_indicators)
def test_volatility(func: Union[DataFrame, Series], pandas_type, dim, sum_result):
    """Test volatility indicators."""

    assert isinstance(func, pandas_type)
    assert func.shape == dim
    result = func.values[~isnan(func.values)].sum()
    assert round(result, 5) == sum_result


@pytest.mark.parametrize("func, pandas_type, dim, sum_result", momentum_indicators)
def test_momentum(func: Union[DataFrame, Series], pandas_type, dim, sum_result):
    """Test momentum indicators."""

    assert isinstance(func, pandas_type)
    assert func.shape == dim
    result = func.values[~isnan(func.values)].sum()
    assert round(result, 5) == sum_result
