"""Volatility indicators"""


from numpy import zeros, nan, where
from pandas import DataFrame, Series, concat


def bollinger_bands(close: Series, window: int = 20, window_dev: int = 2) -> DataFrame:
    """Bollinger Bands

    https://school.stockcharts.com/doku.php?id=technical_indicators:bollinger_bands

    Args:
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
        window_dev(int): n factor standard deviation
        fillna(bool): if True, fill nan values.
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

    true_range = _true_range(high, low, close.shift(1))
    atr = zeros(len(close))
    atr[:] = nan
    atr[window - 1] = true_range[0:window].mean()
    for i in range(window, len(atr)):
        atr[i] = (atr[i - 1] * (window - 1) + true_range.iloc[i]) / float(window)
    return Series(data=atr, index=true_range.index)


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
    offset: int = 0,
    fillna: bool = False,
):
    """Donchian Channel

    https://www.investopedia.com/terms/d/donchianchannels.asp

    Args:
        high(pandas.Series): dataset 'High' column.
        low(pandas.Series): dataset 'Low' column.
        close(pandas.Series): dataset 'Close' column.
        window(int): n period.
    """

    def _run(self):
        self._min_periods = 1 if self._fillna else self._window
        self._hband = self._high.rolling(
            self._window, min_periods=self._min_periods
        ).max()
        self._lband = self._low.rolling(
            self._window, min_periods=self._min_periods
        ).min()

    def donchian_channel_hband(self) -> Series:
        """Donchian Channel High Band

        Returns:
            pandas.Series: New feature generated.
        """
        hband = self._check_fillna(self._hband, value=-1)
        if self._offset != 0:
            hband = hband.shift(self._offset)
        return Series(hband, name="dchband")

    def donchian_channel_lband(self) -> Series:
        """Donchian Channel Low Band

        Returns:
            pandas.Series: New feature generated.
        """
        lband = self._check_fillna(self._lband, value=-1)
        if self._offset != 0:
            lband = lband.shift(self._offset)
        return Series(lband, name="dclband")

    def donchian_channel_mband(self) -> Series:
        """Donchian Channel Middle Band

        Returns:
            pandas.Series: New feature generated.
        """
        mband = ((self._hband - self._lband) / 2.0) + self._lband
        mband = self._check_fillna(mband, value=-1)
        if self._offset != 0:
            mband = mband.shift(self._offset)
        return Series(mband, name="dcmband")

    def donchian_channel_wband(self) -> Series:
        """Donchian Channel Band Width

        Returns:
            pandas.Series: New feature generated.
        """
        mavg = self._close.rolling(self._window, min_periods=self._min_periods).mean()
        wband = ((self._hband - self._lband) / mavg) * 100
        wband = self._check_fillna(wband, value=0)
        if self._offset != 0:
            wband = wband.shift(self._offset)
        return Series(wband, name="dcwband")

    def donchian_channel_pband(self) -> Series:
        """Donchian Channel Percentage Band

        Returns:
            pandas.Series: New feature generated.
        """
        pband = (self._close - self._lband) / (self._hband - self._lband)
        pband = self._check_fillna(pband, value=0)
        if self._offset != 0:
            pband = pband.shift(self._offset)
        return Series(pband, name="dcpband")


def _true_range(high: Series, low: Series, prev_close: Series) -> Series:
    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    return DataFrame(data={"tr1": tr1, "tr2": tr2, "tr3": tr3}).max(axis=1)
