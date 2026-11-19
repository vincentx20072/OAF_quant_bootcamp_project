"""P2: hand-built 12-1 momentum winners-minus-losers. Owner: Dev 2. Task T08 replaces these stubs.

Rules (from PLAN.md): at each month-end rank STOCKS by the return from 12 months ago to 1 month ago
(skip the latest month); top third = winners, bottom third = losers, equal weight; hold the next month.
No look-ahead: weights for month m use only closes up to the last trading day of month m-1.
"""

from __future__ import annotations

import pandas as pd

from .contract import Prices, SplitReturns


def momentum_signal(close: pd.DataFrame) -> pd.DataFrame:
    """Month-end 12-1 momentum per ticker (index = month-end dates). STUB: all NaN."""
    month_ends = close.resample("ME").last().index
    return pd.DataFrame(float("nan"), index=month_ends, columns=close.columns)


def wml_weights(signal: pd.DataFrame, daily_index: pd.DatetimeIndex) -> pd.DataFrame:
    """Daily weights (+1/n winners, -1/n losers) for each trading day. STUB: all zero."""
    return pd.DataFrame(0.0, index=daily_index, columns=signal.columns)


def wml_split(prices: Prices, split: SplitReturns) -> SplitReturns:
    """WML portfolio's overnight and intraday returns, one column 'WML'. STUB: zeros."""
    weights = wml_weights(momentum_signal(prices.close), split.overnight.index)
    cols = list(weights.columns)
    on = (weights * split.overnight[cols]).sum(axis=1).to_frame("WML")
    intra = (weights * split.intraday[cols]).sum(axis=1).to_frame("WML")
    return SplitReturns(on, intra)
