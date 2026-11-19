"""Price loading and caching. Owner: Dev 1. Task T02 finishes this module."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

from .contract import DEFAULT_START, UNIVERSE, Prices

REPO_ROOT = Path(__file__).resolve().parents[2]


def cache_dir() -> Path:
    return Path(os.environ.get("OI_DATA_DIR", REPO_ROOT / "data" / "cache"))


def _cache_paths(directory: Path) -> tuple[Path, Path]:
    return directory / "open.csv.gz", directory / "close.csv.gz"


def load_prices(
    tickers: list[str] | None = None,
    start: str | None = None,
    end: str | None = None,
    refresh: bool = False,
) -> Prices:
    """Adjusted Open/Close for ``tickers``. Uses the cache unless ``refresh`` or tickers are missing.

    TODO(T02): verify that auto_adjust adjusts Open as well as Close; add retries for rate limits.
    """
    tickers = tickers or UNIVERSE
    start = start or os.environ.get("OI_START", DEFAULT_START)
    o_path, c_path = _cache_paths(cache_dir())
    if not refresh and o_path.exists() and c_path.exists():
        o = pd.read_csv(o_path, index_col=0, parse_dates=True)
        c = pd.read_csv(c_path, index_col=0, parse_dates=True)
        if set(tickers) <= set(c.columns):
            o, c = o.loc[start:end, tickers], c.loc[start:end, tickers]
            prices = Prices(o, c)
            prices.validate()
            return prices

    import yfinance as yf  # imported lazily so tests run without network

    raw = yf.download(tickers, start=start, end=end, auto_adjust=True, progress=False, group_by="column")
    o = raw["Open"][tickers].sort_index()
    c = raw["Close"][tickers].sort_index()
    o.index = pd.DatetimeIndex(o.index).tz_localize(None)
    c.index = pd.DatetimeIndex(c.index).tz_localize(None)
    o_path.parent.mkdir(parents=True, exist_ok=True)
    o.to_csv(o_path)
    c.to_csv(c_path)
    prices = Prices(o, c)
    prices.validate()
    return prices


def synthetic_prices(
    tickers: list[str] | None = None,
    start: str = "2013-01-01",
    end: str = "2024-12-31",
    seed: int = 0,
    overnight_drift: float = 0.0004,
    intraday_drift: float = 0.0,
) -> Prices:
    """Random prices with a built-in overnight premium. For tests and offline runs only."""
    tickers = tickers or UNIVERSE
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range(start, end)
    n, k = len(idx), len(tickers)
    on = overnight_drift + 0.006 * rng.standard_normal((n, k))
    intra = intraday_drift + 0.009 * rng.standard_normal((n, k))
    log_close = np.cumsum(on + intra, axis=0) + np.log(100.0)
    log_open = log_close - intra
    o = pd.DataFrame(np.exp(log_open), index=idx, columns=tickers)
    c = pd.DataFrame(np.exp(log_close), index=idx, columns=tickers)
    return Prices(o, c)


def check_prices(prices: Prices) -> dict[str, dict[str, int]]:
    """Per-ticker data-quality counts. TODO(T02): flag stale opens (Open == previous Close) and big gaps."""
    report: dict[str, dict[str, int]] = {}
    for t in prices.tickers:
        report[t] = {
            "rows": int(prices.close[t].notna().sum()),
            "missing_open": int(prices.open[t].isna().sum() - prices.close[t].isna().sum()),
        }
    return report
