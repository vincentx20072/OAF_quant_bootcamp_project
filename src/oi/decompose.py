"""Overnight / intraday decomposition. Owner: Dev 1. Task T03 finishes this module."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .contract import Prices, SplitReturns


def split_returns(prices: Prices) -> SplitReturns:
    """overnight_t = ln(O_t / C_{t-1}); intraday_t = ln(C_t / O_t). First row dropped."""
    overnight = np.log(prices.open / prices.close.shift(1)).iloc[1:]
    intraday = np.log(prices.close / prices.open).iloc[1:]
    return SplitReturns(overnight, intraday)


def cumulative(returns: pd.DataFrame | pd.Series) -> pd.DataFrame | pd.Series:
    """Cumulative log return (NaN treated as 0 so lines start where data starts)."""
    return returns.fillna(0.0).cumsum()


def equal_weight(split: SplitReturns, columns: list[str], label: str = "EW") -> SplitReturns:
    """Equal-weight basket of ``columns`` (mean of log returns: a daily-rebalanced approximation)."""
    on = split.overnight[columns].mean(axis=1).to_frame(label)
    intra = split.intraday[columns].mean(axis=1).to_frame(label)
    return SplitReturns(on, intra)


def gap_by_year(split: SplitReturns) -> pd.DataFrame:
    """Calendar-year sum of overnight minus intraday log returns, per column. TODO(T03): add tests."""
    gap = split.overnight - split.intraday
    return gap.groupby(gap.index.year).sum(min_count=1)
