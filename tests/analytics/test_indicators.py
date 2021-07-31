"""Test indicators"""

from typing import Union

import pytest
from numpy import isnan
from pandas import DataFrame, Series
from src.analytics import indicators as ind
from tests.test_data.raw_data.analytics import indices

indices_df = DataFrame(indices)
_high = indices_df["High"]
_low = indices_df["Low"]
_open = indices_df["Open"]
_close = indices_df["Close"]
_volume = indices_df["High"]

volatility_indicators = (
    (ind.bollinger_bands(_close), (22, 4), 500.08004),
    (ind.average_true_range(_high, _low, _close), (22, 1), 4.36237),
    (ind.keltner_channel(_high, _low, _close), (22, 7), 5143.7484),
    (
        ind.keltner_channel(_high, _low, _close, original=False),
        (22, 7),
        729.18664,
    ),
    (ind.donchian_channel(_high, _low, _close), (22, 5), 731.40188),
    (ind.ulcer_index(_close), (22, 1), 2.83994),
)

momentum_indicators = (
    (ind.relative_strenght_index(_close), (22, 1), 599.60509),
    (ind.true_strength_index(_close), (22, 1), 0.0),
    (ind.ultimate_oscillator(_high, _low, _close), (22, 1), 0.0),
    (ind.stochastic_oscillator(_high, _low, _close), (22, 2), 1304.04195),
    (ind.kama(_close), (22, 1), 1023.09199),
    (ind.rate_of_change(_close), (22, 1), 44.67513),
    (ind.awesome_oscillator(_high, _low), (22, 1), 0.0),
    (ind.williams_r(_high, _low, _close), (22, 1), -157.86866),
    (ind.stochastic_rsi(_close), (22, 3), 0.0),
    (ind.percentage_price_oscillator(_close), (22, 3), 0.0),
    (ind.percentage_volume_oscillator(_close), (22, 3), 0.0),
)

volume_indicators = (
    (ind.acc_dist_index(_high, _low, _close, _volume), (22, 1), 6014.10029),
    (ind.on_balance_volume(_close, _volume), (22, 1), 7027.79767),
    (ind.chaikin_money_flow(_high, _low, _close, _volume), (22, 1), 0.67394),
    (ind.force_index(_close, _volume), (22, 1), 144.46251),
    (ind.ease_of_movement(_high, _low, _volume), (22, 2), 10461678.24221),
    (ind.volume_price_trend(_close, _volume), (22, 1), 7.09254),
    (ind.negative_volume_index(_close, _volume), (22, 1), 21814.00056),
    (ind.money_flow_index(_high, _low, _close, _volume), (22, 1), 553.76938),
    (
        ind.volume_weighted_average_price(_high, _low, _close, _volume),
        (22, 1),
        703.33201,
    ),
)

trend_indicators = (
    (ind.aroon(_close), (22, 3), 0.0),
    (ind.moving_average_convergence_divergence(_close), (22, 3), 0.0),
    (ind.exponential_moving_average(_close), (22, 1), 704.61361),
    (ind.simple_moving_average(_close, 5), (22, 1), 1404.45551),
    (ind.weighted_moving_average(_close), (22, 1), 1100.38284),
    (ind.trix(_close), (22, 1), 0.0),
    (ind.mass_index(_high, _low), (22, 1), 0.0),
    (ind.ichimoku(_high, _low), (22, 4), 2760.11874),
    (ind.kst_oscillator(_close), (22, 3), 236.76165),
    (ind.detrended_price_oscillator(_close), (22, 1), 1.41624),
    (ind.commodity_channel_index(_high, _low, _close), (22, 1), 286.58953),
    #  (ind.average_directional_movement(_high, _low, _close), (22, 3), 6014.10029),
    (ind.vortex(_high, _low, _close), (22, 3), 18.75975),
    (ind.parabolic_stop_and_reverse(_high, _low, _close), (22, 5), 3194.06112),
    (ind.schaff_trend_cycle(_close), (22, 1), 0.0),
)


@pytest.mark.parametrize("func, dim, sum_result", volatility_indicators)
def test_volatility(func: Union[DataFrame, Series], dim, sum_result):
    """Test volatility indicators."""

    assert isinstance(func, DataFrame)
    assert func.shape == dim
    result = func.values[~isnan(func.values)].sum()
    assert round(result, 5) == sum_result


@pytest.mark.parametrize("func, dim, sum_result", momentum_indicators)
def test_momentum(func: Union[DataFrame, Series], dim, sum_result):
    """Test momentum indicators."""

    assert isinstance(func, DataFrame)
    assert func.shape == dim
    result = func.values[~isnan(func.values)].sum()
    assert round(result, 5) == sum_result


@pytest.mark.parametrize("func, dim, sum_result", volume_indicators)
def test_volume(func: Union[DataFrame, Series], dim, sum_result):
    """Test momentum indicators."""

    assert isinstance(func, DataFrame)
    assert func.shape == dim
    result = func.values[~isnan(func.values)].sum()
    assert round(result, 5) == sum_result


@pytest.mark.parametrize("func, dim, sum_result", trend_indicators)
def test_trend(func: Union[DataFrame, Series], dim, sum_result):
    """Test trend indicators."""

    assert isinstance(func, DataFrame)
    assert func.shape == dim
    result = func.values[~isnan(func.values)].sum()
    assert round(result, 5) == sum_result
