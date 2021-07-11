"""Utilities for analytic tests"""


from typing import List
from pandas import Series


def get_df_results(aapl: float, tsla: float) -> List[Series]:
    """Get benchmark dfs."""

    return [Series({"AAPL": aapl, "TSLA": tsla}), Series({"AAPL": aapl})]
