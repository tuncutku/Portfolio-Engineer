"""Trend indicators"""

# pylint: disable=too-many-locals, too-many-arguments, too-many-statements, too-many-branches, line-too-long

from numpy import argmax, argmin, mean

# from numpy import zeros, concatenate
from pandas import DataFrame, Series, concat

from src.analytics.indicators.utils import ema, sma, true_range

#  from src.analytics.indicators.utils import get_max, get_min


def aroon(close: Series, window: int = 25) -> DataFrame:
    """Aroon Indicator

    Identify when trends are likely to change direction.

    Aroon Up = ((N - Days Since N-day High) / N) x 100
    Aroon Down = ((N - Days Since N-day Low) / N) x 100
    Aroon Indicator = Aroon Up - Aroon Down

    https://www.investopedia.com/terms/a/aroon.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    rolling_close = close.rolling(window, min_periods=window)
    aroon_up = rolling_close.apply(
        lambda x: float(argmax(x) + 1) / window * 100, raw=True
    )
    aroon_down = rolling_close.apply(
        lambda x: float(argmin(x) + 1) / window * 100, raw=True
    )

    aroon_up = Series(aroon_up, name="aroon_up")
    aroon_down = Series(aroon_down, name="aroon_down")
    aroon_diff = Series(aroon_up - aroon_down, name="aroon_diff")
    return concat([aroon_up, aroon_down, aroon_diff], axis=1)


def moving_average_convergence_divergence(
    close: Series,
    window_slow: int = 26,
    window_fast: int = 12,
    window_sign: int = 9,
) -> DataFrame:
    """Moving Average Convergence Divergence (MACD)

    Is a trend-following momentum indicator that shows the relationship between
    two moving averages of prices.

    https://school.stockcharts.com/doku.php?id=technical_indicators:moving_average_convergence_divergence_macd

    Args:
        close(pandas.Series): dataset 'Close' column.
        window_fast(int): n period short-term.
        window_slow(int): n period long-term.
        window_sign(int): n period to signal.
    """

    emafast = ema(close, window_fast)
    emaslow = ema(close, window_slow)
    macd = Series(emafast - emaslow, name="MACD")
    macd_signal = Series(ema(macd, window_sign), name="MACD_signal")
    macd_diff = Series(macd - macd_signal, name="MACD_diff")
    return concat([macd, macd_signal, macd_diff], axis=1)


def exponential_moving_average(close: Series, window: int = 14) -> DataFrame:
    """EMA - Exponential Moving Average

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    return Series(ema(close, window), name="ema").to_frame()


def simple_moving_average(close: Series, window: int) -> DataFrame:
    """SMA - Simple Moving Average

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    return Series(sma(close, window), name="sma").to_frame()


def weighted_moving_average(close: Series, window: int = 9) -> DataFrame:
    """WMA - Weighted Moving Average

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    _weight = Series([i * 2 / (window * (window + 1)) for i in range(1, window + 1)])

    def _weighted_average(series: Series):
        return (_weight * series).sum()

    wma = close.rolling(window).apply(_weighted_average, raw=True)
    return Series(wma, name="wma").to_frame()


def trix(close: Series, window: int = 15) -> DataFrame:
    """Trix (TRIX)

    Shows the percent rate of change of a triple exponentially smoothed moving
    average.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:trix

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    ema1 = ema(close, window)
    ema2 = ema(ema1, window)
    ema3 = ema(ema2, window)
    _trix = (ema3 - ema3.shift(1, fill_value=ema3.mean())) / ema3.shift(
        1, fill_value=ema3.mean()
    )
    return Series(_trix * 100, name="trix").to_frame()


def mass_index(
    high: Series,
    low: Series,
    window_fast: int = 9,
    window_slow: int = 25,
) -> DataFrame:
    """Mass Index (MI)

    It uses the high-low range to identify trend reversals based on range
    expansions. It identifies range bulges that can foreshadow a reversal of
    the current trend.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:mass_index

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        window_fast(int): fast period value.
        window_slow(int): slow period value.
    """

    ema1 = ema(high - low, window_fast)
    ema2 = ema(ema1, window_fast)
    mass = ema1 / ema2
    mass = mass.rolling(window_slow, min_periods=window_slow).sum()
    return Series(mass, name="mass_index").to_frame()


def ichimoku(
    high: Series,
    low: Series,
    window1: int = 9,
    window2: int = 26,
    window3: int = 52,
    visual: bool = False,
) -> DataFrame:
    """Ichimoku Kinkō Hyō (Ichimoku)

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ichimoku_cloud

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        window1(int): n1 low period.
        window2(int): n2 medium period.
        window3(int): n3 high period.
        visual(bool): if True, shift n2 values.
    """

    conv = 0.5 * (
        high.rolling(window1, min_periods=window1).max()
        + low.rolling(window1, min_periods=window1).min()
    )
    base = 0.5 * (
        high.rolling(window2, min_periods=window2).max()
        + low.rolling(window2, min_periods=window2).min()
    )
    conv = Series(conv, name="ichimoku_conv")
    base = Series(base, name="ichimoku_base")

    spana = 0.5 * (conv + base)
    spana = spana.shift(window2, fill_value=spana.mean()) if visual else spana
    spana = Series(spana, name="ichimoku_a")

    spanb = 0.5 * (
        high.rolling(window3, min_periods=0).max()
        + low.rolling(window3, min_periods=0).min()
    )
    spanb = spanb.shift(window2, fill_value=spanb.mean()) if visual else spanb
    spanb = Series(spanb, name="ichimoku_b")
    return concat([conv, base, spana, spanb], axis=1)


def kst_oscillator(
    close: Series,
    roc1: int = 10,
    roc2: int = 15,
    roc3: int = 20,
    roc4: int = 30,
    window1: int = 10,
    window2: int = 10,
    window3: int = 10,
    window4: int = 15,
    nsig: int = 9,
) -> DataFrame:
    """KST Oscillator (KST Signal)

    It is useful to identify major stock market cycle junctures because its
    formula is weighed to be more greatly influenced by the longer and more
    dominant time spans, in order to better reflect the primary swings of stock
    market cycle.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:know_sure_thing_kst

    Args:
        close(pandas.Series): dataset 'Close' column.
        roc1(int): roc1 period.
        roc2(int): roc2 period.
        roc3(int): roc3 period.
        roc4(int): roc4 period.
        window1(int): n1 smoothed period.
        window2(int): n2 smoothed period.
        window3(int): n3 smoothed period.
        window4(int): n4 smoothed period.
        nsig(int): n period to signal.
    """

    rocma1 = (
        (
            (close - close.shift(roc1, fill_value=close.mean()))
            / close.shift(roc1, fill_value=close.mean())
        )
        .rolling(window1, min_periods=window1)
        .mean()
    )
    rocma2 = (
        (
            (close - close.shift(roc2, fill_value=close.mean()))
            / close.shift(roc2, fill_value=close.mean())
        )
        .rolling(window2, min_periods=window2)
        .mean()
    )
    rocma3 = (
        (
            (close - close.shift(roc3, fill_value=close.mean()))
            / close.shift(roc3, fill_value=close.mean())
        )
        .rolling(window3, min_periods=window3)
        .mean()
    )
    rocma4 = (
        (
            (close - close.shift(roc4, fill_value=close.mean()))
            / close.shift(roc4, fill_value=close.mean())
        )
        .rolling(window4, min_periods=window4)
        .mean()
    )
    kst = Series(100 * (rocma1 + 2 * rocma2 + 3 * rocma3 + 4 * rocma4), name="kst")
    kst_sig = Series(kst.rolling(nsig, min_periods=0).mean(), name="kst_sig")
    kst_diff = Series(kst - kst_sig, name="kst_diff")
    return concat([kst, kst_sig, kst_diff], axis=1)


def detrended_price_oscillator(close: Series, window: int = 20) -> DataFrame:
    """Detrended Price Oscillator (DPO)

    Is an indicator designed to remove trend from price and make it easier to
    identify cycles.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:detrended_price_osci

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    dpo = (
        close.shift(int((0.5 * window) + 1), fill_value=close.mean())
        - close.rolling(window, min_periods=window).mean()
    )
    return Series(dpo, name="dpo" + str(window)).to_frame()


def commodity_channel_index(
    high: Series,
    low: Series,
    close: Series,
    window: int = 20,
    constant: float = 0.015,
) -> DataFrame:
    """Commodity Channel Index (CCI)

    CCI measures the difference between a security's price change and its
    average price change. High positive readings indicate that prices are well
    above their average, which is a show of strength. Low negative readings
    indicate that prices are well below their average, which is a show of
    weakness.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:commodity_channel_index_cci

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
        constant(int): constant.
    """

    def _mad(series):
        return mean(abs(series - mean(series)))

    typical_price = (high + low + close) / 3.0
    cci = (typical_price - typical_price.rolling(window, min_periods=window).mean()) / (
        constant * typical_price.rolling(window, min_periods=window).apply(_mad, True)
    )
    return Series(cci, name="cci").to_frame()


# def average_directional_movement(
#     high: Series,
#     low: Series,
#     close: Series,
#     window: int = 14,
# ) -> DataFrame:
#     """Average Directional Movement Index (ADX)

#     The Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI)
#     are derived from smoothed averages of these differences, and measure trend
#     direction over time. These two indicators are often referred to
#     collectively as the Directional Movement Indicator (DMI).

#     The Average Directional Index (ADX) is in turn derived from the smoothed
#     averages of the difference between +DI and -DI, and measures the strength
#     of the trend (regardless of direction) over time.

#     Using these three indicators together, chartists can determine both the
#     direction and strength of the trend.

#     http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_directional_index_adx

#     Args:
#         high(pandas.Series): dataset 'High' column.
#         low(pandas.Series): dataset 'Low' column.
#         close(pandas.Series): dataset 'Close' column.
#         window(int): n period.
#     """

#     if window == 0:
#         raise ValueError("window may not be 0")

#     close_shift = close.shift(1)
#     pdm = get_max(high, close_shift)
#     pdn = get_min(low, close_shift)
#     diff_directional_movement = pdm - pdn

#     trs_initial = zeros(window - 1)
#     trs = zeros(len(close) - (window - 1))
#     trs[0] = diff_directional_movement.dropna()[0:window].sum()
#     diff_directional_movement = diff_directional_movement.reset_index(drop=True)

#     for i in range(1, len(trs) - 1):
#         trs[i] = (
#             trs[i - 1]
#             - (trs[i - 1] / float(window))
#             + diff_directional_movement[window + i]
#         )

#     diff_up = high - high.shift(1)
#     diff_down = low.shift(1) - low
#     pos = abs(((diff_up > diff_down) & (diff_up > 0)) * diff_up)
#     neg = abs(((diff_down > diff_up) & (diff_down > 0)) * diff_down)

#     dip = zeros(len(close) - (window - 1))
#     dip[0] = pos.dropna()[0:window].sum()

#     pos = pos.reset_index(drop=True)

#     for i in range(1, len(dip) - 1):
#         dip[i] = dip[i - 1] - (dip[i - 1] / float(window)) + pos[window + i]

#     din = zeros(len(close) - (window - 1))
#     din[0] = neg.dropna()[0:window].sum()

#     neg = neg.reset_index(drop=True)

#     for i in range(1, len(din) - 1):
#         din[i] = din[i - 1] - (din[i - 1] / float(window)) + neg[window + i]

#     # Minus Directional Indicator (-DI)
#     din = zeros(len(close))
#     for i in range(1, len(trs) - 1):
#         din[i + window] = 100 * (din[i] / trs[i])

#     adx_neg = Series(din, index=close.index, name="adx_neg")

#     # Plus Directional Indicator (+DI)
#     dip = zeros(len(close))
#     for i in range(1, len(trs) - 1):
#         dip[i + window] = 100 * (dip[i] / trs[i])

#     adx_pos = Series(dip, index=close.index, name="adx_pos")

#     # Average Directional Index (ADX)
#     dip = zeros(len(trs))
#     for i in enumerate(trs):
#         dip[i] = 100 * (dip[i] / trs[i])

#     din = zeros(len(trs))
#     for i in enumerate(trs):
#         din[i] = 100 * (din[i] / trs[i])

#     directional_index = 100 * abs((dip - din) / (dip + din))
#     adx_series = zeros(len(trs))
#     adx_series[window] = directional_index[0:window].mean()

#     for i in range(window + 1, len(adx_series)):
#         adx_series[i] = (
#             (adx_series[i - 1] * (window - 1)) + directional_index[i - 1]
#         ) / float(window)

#     adx_series = concatenate((trs_initial, adx_series), axis=0)
#     adx_series = Series(data=adx_series, index=close.index)
#     adx = Series(adx_series, name="adx")
#     return concat([adx_neg, adx_pos, adx], axis=1)


def vortex(
    high: Series,
    low: Series,
    close: Series,
    window: int = 14,
) -> DataFrame:
    """Vortex Indicator (VI)

    It consists of two oscillators that capture positive and negative trend
    movement. A bullish signal triggers when the positive trend indicator
    crosses above the negative trend indicator or a key level.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:vortex_indicator

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    close_shift = close.shift(1, fill_value=close.mean())
    _true_range = true_range(high, low, close_shift)
    trn = _true_range.rolling(window, min_periods=window).sum()
    vmp = abs(high - low.shift(1))
    vmm = abs(low - high.shift(1))
    vip = Series(vmp.rolling(window, min_periods=window).sum() / trn, name="vip")
    vin = Series(vmm.rolling(window, min_periods=window).sum() / trn, name="vin")
    vid = Series(vip - vin, name="vid")
    return concat([vip, vin, vid], axis=1)


def parabolic_stop_and_reverse(
    high: Series,
    low: Series,
    close: Series,
    step: float = 0.02,
    max_step: float = 0.20,
) -> DataFrame:
    """Parabolic Stop and Reverse (Parabolic SAR)

    The Parabolic Stop and Reverse, more commonly known as the
    Parabolic SAR,is a trend-following indicator developed by
    J. Welles Wilder. The Parabolic SAR is displayed as a single
    parabolic line (or dots) underneath the price bars in an uptrend,
    and above the price bars in a downtrend.

    https://school.stockcharts.com/doku.php?id=technical_indicators:parabolic_sar

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        step(float): the Acceleration Factor used to compute the SAR.
        max_step(float): the maximum value allowed for the Acceleration Factor.
    """

    up_trend = True
    acceleration_factor = step
    up_trend_high = high.iloc[0]
    down_trend_low = low.iloc[0]

    psar = close.copy()
    psar_up = Series(index=psar.index, dtype="float64")
    psar_down = Series(index=psar.index, dtype="float64")

    for i in range(2, len(close)):
        reversal = False

        max_high = high.iloc[i]
        min_low = low.iloc[i]

        if up_trend:
            psar.iloc[i] = psar.iloc[i - 1] + (
                acceleration_factor * (up_trend_high - psar.iloc[i - 1])
            )

            if min_low < psar.iloc[i]:
                reversal = True
                psar.iloc[i] = up_trend_high
                down_trend_low = min_low
                acceleration_factor = step
            else:
                if max_high > up_trend_high:
                    up_trend_high = max_high
                    acceleration_factor = min(acceleration_factor + step, max_step)

                low1 = low.iloc[i - 1]
                low2 = low.iloc[i - 2]
                if low2 < psar.iloc[i]:
                    psar.iloc[i] = low2
                elif low1 < psar.iloc[i]:
                    psar.iloc[i] = low1
        else:
            psar.iloc[i] = psar.iloc[i - 1] - (
                acceleration_factor * (psar.iloc[i - 1] - down_trend_low)
            )

            if max_high > psar.iloc[i]:
                reversal = True
                psar.iloc[i] = down_trend_low
                up_trend_high = max_high
                acceleration_factor = step
            else:
                if min_low < down_trend_low:
                    down_trend_low = min_low
                    acceleration_factor = min(acceleration_factor + step, max_step)

                high1 = high.iloc[i - 1]
                high2 = high.iloc[i - 2]
                if high2 > psar.iloc[i]:
                    psar[i] = high2
                elif high1 > psar.iloc[i]:
                    psar.iloc[i] = high1

        up_trend = up_trend != reversal  # XOR

        if up_trend:
            psar_up.iloc[i] = psar.iloc[i]
        else:
            psar_down.iloc[i] = psar.iloc[i]

    psar = Series(psar, name="psar")
    psar_up = Series(psar_up, name="psarup")
    psar_down = Series(psar_down, name="psardown")

    indicator = psar_up.where(psar_up.notnull() & psar_up.shift(1).isnull(), 0)
    indicator = indicator.where(indicator == 0, 1)
    psar_up_ind = Series(indicator, index=close.index, name="psariup")

    indicator = psar_up.where(psar_down.notnull() & psar_down.shift(1).isnull(), 0)
    indicator = indicator.where(indicator == 0, 1)
    psar_down_ind = Series(indicator, index=close.index, name="psaridown")
    return concat([psar, psar_up, psar_down, psar_up_ind, psar_down_ind], axis=1)


def schaff_trend_cycle(
    close: Series,
    window_slow: int = 50,
    window_fast: int = 23,
    cycle: int = 10,
    smooth1: int = 3,
    smooth2: int = 3,
) -> DataFrame:
    """Schaff Trend Cycle (STC)

    The Schaff Trend Cycle (STC) is a charting indicator that
    is commonly used to identify market trends and provide buy
    and sell signals to traders. Developed in 1999 by noted currency
    trader Doug Schaff, STC is a type of oscillator and is based on
    the assumption that, regardless of time frame, currency trends
    accelerate and decelerate in cyclical patterns.

    https://www.investopedia.com/articles/forex/10/schaff-trend-cycle-indicator.asp

    Args:
        close(pandas.Series): dataset 'Close' column.
        window_fast(int): n period short-term.
        window_slow(int): n period long-term.
        cycle(int): cycle size
        smooth1(int): ema period over stoch_k
        smooth2(int): ema period over stoch_kd
    """

    _emafast = ema(close, window_fast)
    _emaslow = ema(close, window_slow)
    _macd = _emafast - _emaslow

    _macdmin = _macd.rolling(window=cycle).min()
    _macdmax = _macd.rolling(window=cycle).max()
    _stoch_k = 100 * (_macd - _macdmin) / (_macdmax - _macdmin)
    _stoch_d = ema(_stoch_k, smooth1)

    _stoch_d_min = _stoch_d.rolling(window=cycle).min()
    _stoch_d_max = _stoch_d.rolling(window=cycle).max()
    _stoch_kd = 100 * (_stoch_d - _stoch_d_min) / (_stoch_d_max - _stoch_d_min)
    return Series(ema(_stoch_kd, smooth2), name="stc").to_frame()
