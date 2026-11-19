"""Shared types and constants for the whole project.

Owner: Dev 1 (lead). Change this file only after posting
`CONTRACT src/oi/contract.py: <old> -> <new>` on the task board and getting a reply.

Conventions used everywhere:
- Prices are dividend-adjusted (yfinance ``auto_adjust=True``).
- Returns are natural-log returns, one row per trading day.
- overnight_t = ln(Open_t / Close_{t-1});  intraday_t = ln(Close_t / Open_t);
  daily_t = overnight_t + intraday_t = ln(Close_t / Close_{t-1}).
- Annualise with TRADING_DAYS; Sharpe = mean / std * sqrt(TRADING_DAYS), risk-free rate 0.
- A "trade" is one switch of the whole portfolio. Costs are quoted in basis points per trade.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TypedDict

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------- constants

TRADING_DAYS: int = 252
DEFAULT_START: str = "2010-01-01"
COST_BPS: tuple[float, ...] = (0.0, 1.0, 2.0, 5.0)

MARKET: str = "SPY"
INDEX_ETFS: list[str] = ["SPY", "QQQ"]
SECTOR_ETFS: list[str] = ["XLK", "XLF", "XLE", "XLV", "XLI", "XLP", "XLY", "XLU"]

# factor name -> ETF ticker
FACTOR_ETFS: dict[str, str] = {
    "momentum": "MTUM",
    "value": "VLUE",
    "low_vol": "USMV",
    "quality": "QUAL",
    "size": "IWM",
}
OVERNIGHT_FACTORS: list[str] = ["momentum"]
INTRADAY_FACTORS: list[str] = ["value", "low_vol", "quality", "size"]

# 20 US large-caps across sectors. Survivorship bias: these are today's large-caps.
STOCKS: list[str] = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "META", "NVDA", "JPM", "BAC", "XOM", "CVX",
    "JNJ", "PFE", "PG", "KO", "WMT", "HD", "CAT", "DE", "UNH", "V",
]

UNIVERSE: list[str] = list(dict.fromkeys(INDEX_ETFS + SECTOR_ETFS + list(FACTOR_ETFS.values()) + STOCKS))

# Names of the four strategies, in the order they are reported.
STRATEGY_NAMES: tuple[str, ...] = ("all_day_blend", "overnight_leg", "intraday_leg", "switching")

# Top-level keys of outputs/results.json.
RESULTS_KEYS: tuple[str, ...] = (
    "meta", "split_stats", "gap_by_year", "factors", "strategies", "costs", "momentum",
)

# --------------------------------------------------------------------------- types


@dataclass(frozen=True)
class Prices:
    """Adjusted daily prices. Both frames share one DatetimeIndex (tz-naive) and the same columns."""

    open: pd.DataFrame
    close: pd.DataFrame

    @property
    def tickers(self) -> list[str]:
        return list(self.close.columns)

    def validate(self) -> None:
        if not self.open.index.equals(self.close.index):
            raise ValueError("open and close must share the same index")
        if list(self.open.columns) != list(self.close.columns):
            raise ValueError("open and close must share the same columns")
        if not isinstance(self.close.index, pd.DatetimeIndex):
            raise TypeError("index must be a DatetimeIndex")
        if not self.close.index.is_monotonic_increasing:
            raise ValueError("index must be sorted ascending")
        for name, frame in (("open", self.open), ("close", self.close)):
            if (frame.dropna(how="all") <= 0).any().any():
                raise ValueError(f"{name} has zero or negative prices")


@dataclass(frozen=True)
class SplitReturns:
    """Overnight and intraday log returns; same index and columns. Columns are tickers or labels."""

    overnight: pd.DataFrame
    intraday: pd.DataFrame

    @property
    def daily(self) -> pd.DataFrame:
        return self.overnight + self.intraday

    @property
    def columns(self) -> list[str]:
        return list(self.overnight.columns)

    def select(self, columns: list[str]) -> "SplitReturns":
        return SplitReturns(self.overnight[columns], self.intraday[columns])


class StatsRow(TypedDict):
    ann_mean: float   # annualised mean log return
    ann_vol: float    # annualised volatility
    sharpe: float     # ann_mean / ann_vol
    n_days: int


@dataclass(frozen=True)
class StrategyResult:
    """Daily gross log returns of one strategy and how often it switches the whole portfolio."""

    name: str
    gross: pd.Series
    trades_per_day: float

    def net(self, cost_bp: float) -> pd.Series:
        return self.gross - self.trades_per_day * cost_bp / 1e4


@dataclass(frozen=True)
class CostSweep:
    """Sharpe ratio per strategy (rows) per cost in bp per trade (columns), plus break-even costs."""

    sharpe: pd.DataFrame
    breakeven_bp: dict[str, float]


def nan_to_none(x: float) -> float | None:
    """JSON helper: NaN/inf become None."""
    return None if x is None or not np.isfinite(x) else float(x)
