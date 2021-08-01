"""Momentum indicators"""


# pylint: disable=too-many-locals, invalid-name, too-many-arguments

from numpy import zeros, nan, where, roll, isnan
from pandas import DataFrame, Series, concat

from src.analytics.indicators.utils import true_range, ema


def relative_strenght_index(close: Series, window: int = 14) -> DataFrame:
    """Relative Strength Index (RSI)

    Compares the magnitude of recent gains and losses over a specified time
    period to measure speed and change of price movements of a security. It is
    primarily used to attempt to identify overbought or oversold conditions in
    the trading of an asset.

    https://www.investopedia.com/terms/r/rsi.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    diff = close.diff(1)
    up = diff.where(diff > 0, 0.0)
    down = -1 * diff.where(diff < 0, 0.0)
    emaup = up.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    emadn = down.ewm(alpha=1 / window, min_periods=window, adjust=False).mean()
    relative_strength = emaup / emadn
    return Series(
        where(emadn == 0, 100, 100 - (100 / (1 + relative_strength))),
        index=close.index,
        name="rsi",
    ).to_frame()


def true_strength_index(
    close: Series,
    window_slow: int = 20,
    window_fast: int = 10,
) -> DataFrame:
    """True strength index (TSI)

    Shows both trend direction and overbought/oversold conditions.

    https://school.stockcharts.com/doku.php?id=technical_indicators:true_strength_index

    Args:
        close(pandas.Series): dataset 'Close' column.
        window_slow(int): high period.
        window_fast(int): low period.
    """

    diff_close = close - close.shift(1)
    smoothed = (
        diff_close.ewm(span=window_slow, min_periods=window_slow, adjust=False)
        .mean()
        .ewm(span=window_fast, min_periods=window_fast, adjust=False)
        .mean()
    )
    smoothed_abs = (
        abs(diff_close)
        .ewm(span=window_slow, min_periods=window_slow, adjust=False)
        .mean()
        .ewm(span=window_fast, min_periods=window_fast, adjust=False)
        .mean()
    )
    tsi = smoothed / smoothed_abs
    return Series(tsi * 100, name="tsi").to_frame()


def ultimate_oscillator(
    high: Series,
    low: Series,
    close: Series,
    window1: int = 7,
    window2: int = 14,
    window3: int = 28,
    weight1: float = 4.0,
    weight2: float = 2.0,
    weight3: float = 1.0,
) -> DataFrame:
    """Ultimate Oscillator

    Larry Williams' (1976) signal, a momentum oscillator designed to capture
    momentum across three different timeframes.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator

    BP = Close - Minimum(Low or Prior Close).
    TR = Maximum(High or Prior Close)  -  Minimum(Low or Prior Close)
    Average7 = (7-period BP Sum) / (7-period TR Sum)
    Average14 = (14-period BP Sum) / (14-period TR Sum)
    Average28 = (28-period BP Sum) / (28-period TR Sum)

    UO = 100 x [(4 x Average7)+(2 x Average14)+Average28]/(4+2+1)

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window1(int): short period.
        window2(int): medium period.
        window3(int): long period.
        weight1(float): weight of short BP average for UO.
        weight2(float): weight of medium BP average for UO.
        weight3(float): weight of long BP average for UO.
    """

    close_shift = close.shift(1)
    true_range_result = true_range(high, low, close_shift)
    buying_pressure = close - DataFrame({"low": low, "close": close_shift}).min(
        axis=1, skipna=False
    )
    avg_s = (
        buying_pressure.rolling(window1, min_periods=window1).sum()
        / true_range_result.rolling(window1, min_periods=window1).sum()
    )
    avg_m = (
        buying_pressure.rolling(window2, min_periods=window2).sum()
        / true_range_result.rolling(window2, min_periods=window2).sum()
    )
    avg_l = (
        buying_pressure.rolling(window3, min_periods=window3).sum()
        / true_range_result.rolling(window3, min_periods=window3).sum()
    )
    uo = (
        100.0
        * ((weight1 * avg_s) + (weight2 * avg_m) + (weight3 * avg_l))
        / (weight1 + weight2 + weight3)
    )
    return Series(uo, name="uo").to_frame()


def stochastic_oscillator(
    high: Series,
    low: Series,
    close: Series,
    window: int = 14,
    smooth_window: int = 3,
) -> DataFrame:
    """Stochastic Oscillator

    Developed in the late 1950s by George Lane. The stochastic
    oscillator presents the location of the closing price of a
    stock in relation to the high and low range of the price
    of a stock over a period of time, typically a 14-day period.

    https://school.stockcharts.com/doku.php?id=technical_indicators:stochastic_oscillator_fast_slow_and_full

    Args:
        close(pandas.Series): dataset 'Close' column.
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        window(int): n period.
        smooth_window(int): sma period over stoch_k.
    """

    smin = low.rolling(window, min_periods=window).min()
    smax = high.rolling(window, min_periods=window).max()
    stoch_k = 100 * (close - smin) / (smax - smin)
    stoch_d = stoch_k.rolling(smooth_window, min_periods=smooth_window).mean()

    stoch_k = Series(stoch_k, name="stoch_k")
    stoch_d = Series(stoch_d, name="stoch_k_signal")
    return concat([stoch_k, stoch_d], axis=1)


def kama(close: Series, window: int = 10, pow1: int = 2, pow2: int = 30) -> DataFrame:
    """Kaufman's Adaptive Moving Average (KAMA)

    Moving average designed to account for market noise or volatility. KAMA
    will closely follow prices when the price swings are relatively small and
    the noise is low. KAMA will adjust when the price swings widen and follow
    prices from a greater distance. This trend-following indicator can be
    used to identify the overall trend, time turning points and filter price
    movements.

    https://www.tradingview.com/ideas/kama/

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
        pow1(int): number of periods for the fastest EMA constant.
        pow2(int): number of periods for the slowest EMA constant.
    """

    close_values = close.values
    vol = Series(abs(close - roll(close, 1)))

    er_num = abs(close_values - roll(close_values, window))
    er_den = vol.rolling(window, min_periods=window).sum()
    efficiency_ratio = er_num / er_den

    smoothing_constant = (
        (efficiency_ratio * (2.0 / (pow1 + 1) - 2.0 / (pow2 + 1.0)) + 2 / (pow2 + 1.0))
        ** 2.0
    ).values

    _kama = zeros(smoothing_constant.size)
    len_kama = len(_kama)
    first_value = True

    for i in range(len_kama):
        if isnan(smoothing_constant[i]):
            _kama[i] = nan
        elif first_value:
            _kama[i] = close_values[i]
            first_value = False
        else:
            _kama[i] = _kama[i - 1] + smoothing_constant[i] * (
                close_values[i] - _kama[i - 1]
            )

    return Series(_kama, index=close.index, name="kama").to_frame()


def rate_of_change(close: Series, window: int = 12) -> DataFrame:
    """Rate of Change (ROC)

    The Rate-of-Change (ROC) indicator, which is also referred to as simply
    Momentum, is a pure momentum oscillator that measures the percent change in
    price from one period to the next. The ROC calculation compares the current
    price with the price “n” periods ago. The plot forms an oscillator that
    fluctuates above and below the zero line as the Rate-of-Change moves from
    positive to negative. As a momentum oscillator, ROC signals include
    centerline crossovers, divergences and overbought-oversold readings.
    Divergences fail to foreshadow reversals more often than not, so this
    article will forgo a detailed discussion on them. Even though centerline
    crossovers are prone to whipsaw, especially short-term, these crossovers
    can be used to identify the overall trend. Identifying overbought or
    oversold extremes comes naturally to the Rate-of-Change oscillator.

    https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    roc = ((close - close.shift(window)) / close.shift(window)) * 100
    return Series(roc, name="roc").to_frame()


def awesome_oscillator(
    high: Series,
    low: Series,
    window1: int = 5,
    window2: int = 34,
) -> DataFrame:
    """Awesome Oscillator

    From: https://www.tradingview.com/wiki/Awesome_Oscillator_(AO)

    The Awesome Oscillator is an indicator used to measure market momentum. AO
    calculates the difference of a 34 Period and 5 Period Simple Moving
    Averages. The Simple Moving Averages that are used are not calculated
    using closing price but rather each bar's midpoints. AO is generally used
    to affirm trends or to anticipate possible reversals.

    From: https://www.ifcm.co.uk/ntx-indicators/awesome-oscillator

    Awesome Oscillator is a 34-period simple moving average, plotted through
    the central points of the bars (H+L)/2, and subtracted from the 5-period
    simple moving average, graphed across the central points of the bars
    (H+L)/2.

    MEDIAN PRICE = (HIGH+LOW)/2

    AO = SMA(MEDIAN PRICE, 5)-SMA(MEDIAN PRICE, 34)

    where

    SMA — Simple Moving Average.

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        window1(int): short period.
        window2(int): long period.
    """

    median_price = 0.5 * (high + low)
    ao = (
        median_price.rolling(window1, min_periods=window1).mean()
        - median_price.rolling(window2, min_periods=window2).mean()
    )
    return Series(ao, name="ao").to_frame()


def williams_r(
    high: Series,
    low: Series,
    close: Series,
    lbp: int = 14,
) -> DataFrame:
    """Williams %R

    Developed by Larry Williams, Williams %R is a momentum indicator that is
    the inverse of the Fast Stochastic Oscillator. Also referred to as %R,
    Williams %R reflects the level of the close relative to the highest high
    for the look-back period. In contrast, the Stochastic Oscillator reflects
    the level of the close relative to the lowest low. %R corrects for the
    inversion by multiplying the raw value by -100. As a result, the Fast
    Stochastic Oscillator and Williams %R produce the exact same lines, only
    the scaling is different. Williams %R oscillates from 0 to -100.

    Readings from 0 to -20 are considered overbought. Readings from -80 to -100
    are considered oversold.

    Unsurprisingly, signals derived from the Stochastic Oscillator are also
    applicable to Williams %R.

    %R = (Highest High - Close)/(Highest High - Lowest Low) * -100

    Lowest Low = lowest low for the look-back period
    Highest High = highest high for the look-back period
    %R is multiplied by -100 correct the inversion and move the decimal.

    https://school.stockcharts.com/doku.php?id=technical_indicators:williams_r

    The Williams %R oscillates from 0 to -100. When the indicator produces
    readings from 0 to -20, this indicates overbought market conditions. When
    readings are -80 to -100, it indicates oversold market conditions.

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        lbp(int): lookback period.
    """

    # highest high over lookback period lbp
    highest_high = high.rolling(lbp, min_periods=lbp).max()
    # lowest low over lookback period lbp
    lowest_low = low.rolling(lbp, min_periods=lbp).min()
    wr = (highest_high - close) / (highest_high - lowest_low) * -100
    return Series(wr, name="wr").to_frame()


def stochastic_rsi(
    close: Series,
    window: int = 14,
    smooth1: int = 3,
    smooth2: int = 3,
) -> DataFrame:
    """Stochastic RSI

    The StochRSI oscillator was developed to take advantage of both momentum
    indicators in order to create a more sensitive indicator that is attuned to
    a specific security's historical performance rather than a generalized analysis
    of price change.

    https://school.stockcharts.com/doku.php?id=technical_indicators:stochrsi
    https://www.investopedia.com/terms/s/stochrsi.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period
        smooth1(int): moving average of Stochastic RSI
        smooth2(int): moving average of %K
    """

    rsi_index = relative_strenght_index(close, window)
    rsi_index = rsi_index["rsi"]
    lowest_low_rsi = rsi_index.rolling(window).min()
    stochrsi = Series(
        (rsi_index - lowest_low_rsi)
        / (rsi_index.rolling(window).max() - lowest_low_rsi),
        name="stochrsi",
    )
    stochrsi_k = Series(stochrsi.rolling(smooth1).mean(), name="stochrsi_k")
    stochrsi_d_series = Series(stochrsi_k.rolling(smooth2).mean(), name="stochrsi_d")
    return concat([stochrsi, stochrsi_k, stochrsi_d_series], axis=1)


def percentage_price_oscillator(
    close: Series,
    window_slow: int = 26,
    window_fast: int = 12,
    window_sign: int = 9,
) -> DataFrame:
    """
    The Percentage Price Oscillator (PPO) is a momentum oscillator that measures
    the difference between two moving averages as a percentage of the larger moving average.

    https://school.stockcharts.com/doku.php?id=technical_indicators:price_oscillators_ppo

    Args:
        close(pandas.Series): dataset 'Price' column.
        window_slow(int): n period long-term.
        window_fast(int): n period short-term.
        window_sign(int): n period to signal.
    """

    _emafast = ema(close, window_fast)
    _emaslow = ema(close, window_slow)
    ppo = ((_emafast - _emaslow) / _emaslow) * 100
    ppo_signal = ema(ppo, window_sign)
    ppo_hist = ppo - ppo_signal

    ppo = Series(ppo, name=f"PPO_{window_fast}_{window_slow}")
    ppo_signal = Series(ppo_signal, name=f"PPO_sign_{window_fast}_{window_slow}")
    ppo_hist = Series(ppo_hist, name=f"PPO_hist_{window_fast}_{window_slow}")
    return concat([ppo, ppo_signal, ppo_hist], axis=1)


def percentage_volume_oscillator(
    volume: Series,
    window_slow: int = 26,
    window_fast: int = 12,
    window_sign: int = 9,
) -> DataFrame:
    """
    The Percentage Volume Oscillator (PVO) is a momentum oscillator for volume.
    The PVO measures the difference between two volume-based moving averages as a
    percentage of the larger moving average.

    https://school.stockcharts.com/doku.php?id=technical_indicators:percentage_volume_oscillator_pvo

    Args:
        volume(pandas.Series): dataset 'Volume' column.
        window_slow(int): n period long-term.
        window_fast(int): n period short-term.
        window_sign(int): n period to signal.
    """

    _emafast = ema(volume, window_fast)
    _emaslow = ema(volume, window_slow)
    pvo = ((_emafast - _emaslow) / _emaslow) * 100
    pvo_signal = ema(pvo, window_sign)
    pvo_hist = pvo - pvo_signal

    pvo = Series(pvo, name=f"PVO_{window_fast}_{window_slow}")
    pvo_signal = Series(pvo_signal, name=f"PVO_sign_{window_fast}_{window_slow}")
    pvo_hist = Series(pvo_hist, name=f"PVO_hist_{window_fast}_{window_slow}")

    return concat([pvo, pvo_signal, pvo_hist], axis=1)
