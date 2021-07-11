"""Test value adjustments"""

from pandas import DataFrame, concat

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


def test_aggregate():
    """Test aggregate returns and values."""

    return_items = [
        (returns_df, core.Period.daily, DataFrame(analytics.daily_return_raw)),
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
