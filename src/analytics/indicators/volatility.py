"""Volatility indicators"""


from numpy import zeros, nan, where, sqrt
from pandas import DataFrame, Series, concat

from src.analytics.indicators.utils import true_range


def bollinger_bands(close: Series, window: int = 20, window_dev: int = 2) -> DataFrame:
    """Bollinger Bands

    https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_bands

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
        window_dev(int): n factor standard deviation
    """

    mavg = close.rolling(window).mean()
    mstd = close.rolling(window).std(ddof=0)

    hband = Series(mavg + window_dev * mstd, name="hband")
    lband = Series(mavg - window_dev * mstd, name="lband")
    pband = Series((close - lband) / (hband - lband), name="pband")
    wband = Series(((hband - lband) / mavg) * 100, name="wband")

    return concat([hband, lband, pband, wband], axis=1)


def average_true_range(
    high: Series, low: Series, close: Series, window: int = 20
) -> DataFrame:
    """Average True Range (ATR)

    The indicator provide an indication of the degree of price volatility.
    Strong moves, in either direction, are often accompanied by large ranges,
    or large True Ranges.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_true_range_atr

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    true_range_result = true_range(high, low, close.shift(1))
    atr = zeros(len(close))
    atr[:] = nan
    atr[window - 1] = true_range_result[0:window].mean()
    for i in range(window, len(atr)):
        atr[i] = (atr[i - 1] * (window - 1) + true_range_result.iloc[i]) / float(window)
    return Series(atr, index=true_range_result.index, name="Average true range")


def keltner_channel(
    high: Series,
    low: Series,
    close: Series,
    window: int = 20,
    original: bool = True,
) -> DataFrame:
    """KeltnerChannel

    Keltner Channels are a trend following indicator used to identify reversals with
    channel breakouts and channel direction. Channels can also be used to identify
    overbought and oversold levels when the trend is flat.

    https://school.stockcharts.com/doku.php?id=technical_indicators:keltner_channels

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
        window_atr(int): n atr period. Only valid if original_version param is False.
        original_version(bool): if True, use original version as the centerline
            (SMA of typical price) if False, use EMA of close as the centerline. More info:
            https://school.stockcharts.com/doku.php?id=technical_indicators:keltner_channels
    """

    def roll_and_mean(series: Series) -> Series:
        return series.rolling(window, min_periods=0).mean()

    if original:
        tp = roll_and_mean((high + low + close) / 3.0)
        tp_high = roll_and_mean((((4 * high) - (2 * low) + close) / 3.0))
        tp_low = roll_and_mean((((-2 * high) + (4 * low) + close) / 3.0))
    else:
        atr = average_true_range(high, low, close, window)
        tp = close.ewm(span=window, min_periods=window, adjust=False).mean()
        tp_high = tp + (2 * atr)
        tp_low = tp - (2 * atr)

    tp = Series(tp, name="tp")
    tp_high = Series(tp_high, name="tp_high")
    tp_low = Series(tp_low, name="tp_low")
    wband = Series(((tp_high - tp_low) / tp) * 100, name="wband")
    pband = Series((close - tp_low) / (tp_high - tp_low), name="pband")
    hband = Series(where(close > tp_high, 1.0, 0.0), index=close.index, name="hband")
    lband = Series(where(close < tp_low, 1.0, 0.0), index=close.index, name="lband")

    return concat([tp, tp_high, tp_low, hband, lband, pband, wband], axis=1)


def donchian_channel(
    high: Series,
    low: Series,
    close: Series,
    window: int = 20,
) -> DataFrame:
    """Donchian Channel

    https://www.investopedia.com/terms/d/donchianchannels.asp

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    mavg = Series(close.rolling(window).mean(), name="mavg")
    hband = Series(high.rolling(window).max(), name="hband")
    lband = Series(low.rolling(window).min(), name="lband")
    mband = Series(((hband - lband) / 2.0) + lband, name="mband")
    wband = Series(((hband - lband) / mavg) * 100, name="wband")
    pband = Series((close - lband) / (hband - lband), name="pband")

    return concat([mband, hband, lband, pband, wband], axis=1)


def ulcer_index(close: Series, window: int = 20) -> Series:
    """Ulcer Index

    https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ulcer_index

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    _ui_max = close.rolling(window, min_periods=1).max()
    _r_i = 100 * (close - _ui_max) / _ui_max
    _ui_function = lambda x: sqrt((x ** 2 / window).sum())

    ulcer_idx = _r_i.rolling(window).apply(_ui_function, raw=True)
    return Series(ulcer_idx, name="Ulcer index")
