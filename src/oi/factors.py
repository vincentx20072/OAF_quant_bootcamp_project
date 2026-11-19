"""Factor ETFs minus SPY, split overnight / intraday. Owner: Dev 3. Task T05 replaces the stub."""

from __future__ import annotations

import pandas as pd

from .contract import FACTOR_ETFS, MARKET, Prices, SplitReturns


def common_start(prices: Prices, tickers: list[str] | None = None) -> pd.Timestamp:
    """Latest first-valid date across ``tickers`` (default: factor ETFs + market)."""
    tickers = tickers or list(FACTOR_ETFS.values()) + [MARKET]
    return max(prices.close[t].first_valid_index() for t in tickers)


def excess_split(split: SplitReturns, start: pd.Timestamp | None = None) -> SplitReturns:
    """Columns = factor names; values = ETF minus MARKET for each half-day, from ``start``.

    STUB: returns zeros with the right shape. T05: subtract split[MARKET] from each factor ETF.
    """
    idx = split.overnight.index if start is None else split.overnight.loc[start:].index
    zeros = pd.DataFrame(0.0, index=idx, columns=list(FACTOR_ETFS))
    return SplitReturns(zeros, zeros.copy())
