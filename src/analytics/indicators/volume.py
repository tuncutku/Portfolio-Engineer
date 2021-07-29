"""Volatility indicators"""


from numpy import nan, where
from pandas import DataFrame, Series, concat

from src.analytics.indicators.utils import ema


def acc_dist_index(high: Series, low: Series, close: Series, volume: Series) -> Series:
    """Accumulation/Distribution Index (ADI)

    Acting as leading indicator of price movements.

    https://school.stockcharts.com/doku.php?id=technical_indicators:accumulation_distribution_line

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
    """

    clv = ((close - low) - (high - close)) / (high - low)
    clv = clv.fillna(0.0)
    return Series((clv * volume).cumsum(), name="acc dist index")


def on_balance_volume(close: Series, volume: Series) -> Series:
    """On-balance volume (OBV)

    It relates price and volume in the stock market. OBV is based on a
    cumulative total volume.

    https://en.wikipedia.org/wiki/On-balance_volume

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
    """

    obv = where(close < close.shift(1), -volume, volume)
    return Series(obv, index=close.index, name="obv").cumsum()


def chaikin_money_flow(
    high: Series, low: Series, close: Series, volume: Series, window: int = 20
) -> Series:
    """Chaikin Money Flow (CMF)

    It measures the amount of Money Flow Volume over a specific period.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:chaikin_money_flow_cmf

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        window(int): n period.
    """

    mfv = ((close - low) - (high - close)) / (high - low)
    mfv = mfv.fillna(0.0)
    mfv *= volume
    cmf = (
        mfv.rolling(window, min_periods=window).sum()
        / volume.rolling(window, min_periods=window).sum()
    )
    return Series(cmf, name="cmf")


def force_index(
    close: Series,
    volume: Series,
    window: int = 13,
) -> Series:
    """Force Index (FI)

    It illustrates how strong the actual buying or selling pressure is. High
    positive values mean there is a strong rising trend, and low values signify
    a strong downward trend.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:force_index

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        window(int): n period.
    """

    fi_series = (close - close.shift(1)) * volume
    return Series(ema(fi_series, window), name=f"fi_{window}")


def ease_of_movement(
    high: Series, low: Series, volume: Series, window: int = 14
) -> DataFrame:
    """Ease of movement (EoM, EMV)

    It relate an asset's price change to its volume and is particularly useful
    for assessing the strength of a trend.

    https://en.wikipedia.org/wiki/Ease_of_movement

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        volume(pandas.Series): dataset 'Volume' column.
        window(int): n period.
    """

    emv = ((high.diff(1) + low.diff(1)) * (high - low) / (2 * volume)) * 100000000
    eom = Series(emv, name=f"eom_{window}")
    sma_eom = Series(
        emv.rolling(window, min_periods=window).mean(), name=f"sma_eom_{window}"
    )
    return concat([eom, sma_eom], axis=1)


def volume_price_trend(close: Series, volume: Series) -> Series:
    """Volume-price trend (VPT)

    Is based on a running cumulative volume that adds or substracts a multiple
    of the percentage change in share price trend and current volume, depending
    upon the investment's upward or downward movements.

    https://en.wikipedia.org/wiki/Volume%E2%80%93price_trend

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
    """

    vpt = volume * (
        (close - close.shift(1, fill_value=close.mean()))
        / close.shift(1, fill_value=close.mean())
    )
    vpt = vpt.shift(1, fill_value=vpt.mean()) + vpt
    return Series(vpt, name="vpt")


def negative_volume_index(close: Series, volume: Series) -> Series:
    """Negative Volume Index (NVI)

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:negative_volume_inde

    Args:
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
    """

    price_change = close.pct_change()
    vol_decrease = volume.shift(1) > volume
    nvi = Series(data=nan, index=close.index, dtype="float64", name="nvi")
    nvi.iloc[0] = 1000
    for i in range(1, len(nvi)):
        if vol_decrease.iloc[i]:
            nvi.iloc[i] = nvi.iloc[i - 1] * (1.0 + price_change.iloc[i])
        else:
            nvi.iloc[i] = nvi.iloc[i - 1]
    return Series(nvi, name="nvi")


def money_flow_index(
    high: Series,
    low: Series,
    close: Series,
    volume: Series,
    window: int = 14,
) -> Series:
    """Money Flow Index (MFI)

    Uses both price and volume to measure buying and selling pressure. It is
    positive when the typical price rises (buying pressure) and negative when
    the typical price declines (selling pressure). A ratio of positive and
    negative money flow is then plugged into an RSI formula to create an
    oscillator that moves between zero and one hundred.

    http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:money_flow_index_mfi

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        window(int): n period.
    """

    typical_price = (high + low + close) / 3.0
    up_down: int = where(
        typical_price > typical_price.shift(1),
        1,
        where(typical_price < typical_price.shift(1), -1, 0),
    )
    mfr = typical_price * volume * up_down

    # Positive and negative money flow with n periods
    n_positive_mf = mfr.rolling(window, min_periods=window).apply(
        lambda x: sum(where(x >= 0.0, x, 0.0)), raw=True
    )
    n_negative_mf = abs(
        mfr.rolling(window, min_periods=window).apply(
            lambda x: sum(where(x < 0.0, x, 0.0)), raw=True
        )
    )

    # n_positive_mf = where(mf.rolling(window).sum() >= 0.0, mf, 0.0)
    # n_negative_mf = abs(where(mf.rolling(window).sum() < 0.0, mf, 0.0))

    # Money flow index
    mfi = n_positive_mf / n_negative_mf
    return Series(100 - (100 / (1 + mfi)), name=f"mfi_{window}")


def volume_weighted_average_price(
    high: Series,
    low: Series,
    close: Series,
    volume: Series,
    window: int = 14,
) -> Series:
    """Volume Weighted Average Price (VWAP)

    VWAP equals the dollar value of all trading periods divided
    by the total trading volume for the current day.
    The calculation starts when trading opens and ends when it closes.
    Because it is good for the current trading day only,
    intraday periods and data are used in the calculation.

    https://school.stockcharts.com/doku.php?id=technical_indicators:vwap_intraday

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        volume(pandas.Series): dataset 'Volume' column.
        window(int): n period.
    """

    # 1 typical price
    typical_price = (high + low + close) / 3.0
    # 2 typical price * volume
    typical_price_volume = typical_price * volume
    # 3 total price * volume
    total_pv = typical_price_volume.rolling(window, min_periods=window).sum()
    # 4 total volume
    total_volume = volume.rolling(window, min_periods=window).sum()

    return Series(total_pv / total_volume, name=f"vwap_{window}")
