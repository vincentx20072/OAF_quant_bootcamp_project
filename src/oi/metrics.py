"""Return statistics. Owner: Dev 1."""

from __future__ import annotations

import numpy as np
import pandas as pd

from .contract import TRADING_DAYS, SplitReturns, StatsRow


def annualised_stats(returns: pd.Series) -> StatsRow:
    r = returns.dropna()
    n = int(r.size)
    if n < 2:
        return StatsRow(ann_mean=float("nan"), ann_vol=float("nan"), sharpe=float("nan"), n_days=n)
    mean = float(r.mean() * TRADING_DAYS)
    vol = float(r.std(ddof=1) * np.sqrt(TRADING_DAYS))
    sharpe = mean / vol if vol > 0 else float("nan")
    return StatsRow(ann_mean=mean, ann_vol=vol, sharpe=sharpe, n_days=n)


def summary(split: SplitReturns) -> pd.DataFrame:
    """One row per (column, half) with half in {overnight, intraday, daily}."""
    rows = []
    for col in split.columns:
        for half, frame in (("overnight", split.overnight), ("intraday", split.intraday), ("daily", split.daily)):
            rows.append({"series": col, "half": half, **annualised_stats(frame[col])})
    return pd.DataFrame(rows).set_index(["series", "half"])
