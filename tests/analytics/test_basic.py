"""Test basic analytics"""

from pandas import DataFrame, Series, concat

from src import analytics as core
from tests.test_data.market import aapl_series, ry_to_series
from tests.test_data.raw_data import analytics

securities_df = concat([aapl_series, ry_to_series], axis=1)
returns_df = DataFrame(analytics.returns_analytics_raw)
values_df = DataFrame(analytics.values_analytics_raw)


def test_period_filter():
    """Test MTM, QTM and YTD."""

    empty_df = {"AAPL": {}, "RY.TO": {}}

    mtp_df = core.mtd(securities_df)
    qtd_df = core.qtd(securities_df)
    ytd_df = core.ytd(securities_df)

    for new_df in [mtp_df, qtd_df, ytd_df]:
        assert empty_df == new_df.to_dict()


def test_outliers():
    """Test outliers"""

    raw_outliers = core.get_outliers(securities_df)
    assert DataFrame(analytics.outliers).equals(raw_outliers)

    raw_non_outliers = core.remove_outliers(securities_df)
    assert DataFrame(analytics.non_outliers).equals(raw_non_outliers)


def test_cum_operators():
    """Test cumulator operators."""

    periodic_return_df = DataFrame(analytics.periodic_return_raw)

    compsum = core.compsum(periodic_return_df)
    assert DataFrame(analytics.compsum_raw).equals(compsum)

    comp = core.comp(periodic_return_df)
    assert Series(analytics.comp_raw).equals(comp)


def test_aggregate():
    """Test aggregate returns and values."""

    return_items = [
        (returns_df, core.Period.daily, returns_df),
        (returns_df, core.Period.weekly, DataFrame(analytics.weekly_return_raw)),
        (returns_df, core.Period.monthly, DataFrame(analytics.monthly_return_raw)),
        (returns_df, core.Period.yearly, DataFrame(analytics.yearly_return_raw)),
    ]

    for main_df, period, benchmark in return_items:
        result = core.aggregate_returns(main_df, period)
        assert result.equals(benchmark)

    value_items = [
        (values_df, core.Period.daily, values_df),
        (values_df, core.Period.weekly, DataFrame(analytics.weekly_value_raw)),
        (values_df, core.Period.monthly, DataFrame(analytics.monthly_value_raw)),
        (values_df, core.Period.yearly, DataFrame(analytics.yearly_value_raw)),
    ]

    for main_df, period, benchmark in value_items:
        result = core.aggregate_values(main_df, period)
        assert result.equals(benchmark)


def test_consecutive():
    """Test consecutive wins and losses."""

    result = core.consecutive_wins(returns_df)
    assert result.equals(Series({"AAPL": 7, "TSLA": 6}))
    result = core.consecutive_losses(returns_df)
    assert result.equals(Series({"AAPL": 4, "TSLA": 6}))


def test_exposure():
    """Test exposure."""

    result = core.exposure(returns_df)
    assert result.equals(Series({"AAPL": 0.97, "TSLA": 0.97}))


def test_win_average_rate():
    """Test rates."""

    items = [
        ({"AAPL": 0.52691, "TSLA": 0.53955}, core.win_rate),
        ({"AAPL": 0.00200, "TSLA": 0.00525}, core.avg_return),
        ({"AAPL": 0.02010, "TSLA": 0.04252}, core.avg_win),
        ({"AAPL": -0.02208, "TSLA": -0.04078}, core.avg_loss),
    ]

    for benchmark, func in items:
        result = func(returns_df)
        assert result.equals(Series(benchmark))


def test_volatility():
    """Test volatility."""

    result = core.volatility(returns_df)
    assert result.equals(Series({"AAPL": 0.41471, "TSLA": 0.79677}))

    result = core.volatility(returns_df, False)
    assert result.equals(Series({"AAPL": 0.02612, "TSLA": 0.05019}))
