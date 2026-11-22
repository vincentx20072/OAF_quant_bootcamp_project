"""Factor ETFs minus SPY, split overnight / intraday. Owner: Dev 3 (task T05).

For each factor ETF and each half-day, the excess return is the ETF's log return minus SPY's
log return over the same half-day. This is the return of a dollar-neutral position: long the ETF,
short SPY (a log-difference approximation, accurate at daily horizons).
"""

from __future__ import annotations

import pandas as pd

from .contract import FACTOR_ETFS, MARKET, Prices, SplitReturns


def common_start(prices: Prices, tickers: list[str] | None = None) -> pd.Timestamp:
    """Latest first-valid date across ``tickers`` (default: factor ETFs + market)."""
    tickers = tickers or list(FACTOR_ETFS.values()) + [MARKET]
    return max(prices.close[t].first_valid_index() for t in tickers)


def excess_split(split: SplitReturns, start: pd.Timestamp | None = None) -> SplitReturns:
    """Columns = factor names; values = ETF minus MARKET for each half-day, from ``start``.

    ``start`` is normally ``common_start(prices)``. Any row with a missing value in any factor or the
    market is dropped (this removes the youngest ETF's first day, whose overnight return has no
    previous close), so all five columns cover exactly the same days.
    """
    etfs = [FACTOR_ETFS[f] for f in FACTOR_ETFS]
    on, intra = split.overnight, split.intraday
    if start is not None:
        on, intra = on.loc[start:], intra.loc[start:]

    def excess(frame: pd.DataFrame) -> pd.DataFrame:
        out = frame[etfs].sub(frame[MARKET], axis=0)
        out.columns = list(FACTOR_ETFS)
        return out

    ex_on, ex_intra = excess(on), excess(intra)
    keep = ex_on.notna().all(axis=1) & ex_intra.notna().all(axis=1)
    return SplitReturns(ex_on[keep], ex_intra[keep])
