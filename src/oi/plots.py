"""Figures. Owner: Dev 4. Task T09 polishes these (titles, units, source note, colours)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from .contract import CostSweep, SplitReturns, StrategyResult  # noqa: E402
from .decompose import cumulative  # noqa: E402

SOURCE_NOTE = "Source: Yahoo Finance via yfinance, adjusted prices."


def _save(fig: plt.Figure, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.text(0.01, 0.01, SOURCE_NOTE, fontsize=7, color="grey")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_cumulative(split: SplitReturns, column: str, path: Path) -> Path:
    """Headline chart: cumulative overnight vs intraday log return for one series."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(cumulative(split.overnight[column]), label="Overnight (close → open)")
    ax.plot(cumulative(split.intraday[column]), label="Intraday (open → close)")
    ax.axhline(0, color="black", linewidth=0.5)
    ax.set_title(f"{column}: where the return comes from")
    ax.set_ylabel("Cumulative log return")
    ax.legend()
    return _save(fig, path)


def plot_gap_by_year(gap: pd.DataFrame, column: str, path: Path) -> Path:
    """STUB-quality: bar per year of overnight minus intraday."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(gap.index.astype(str), gap[column])
    ax.set_title(f"{column}: overnight minus intraday, by year")
    ax.set_ylabel("Log return")
    return _save(fig, path)


def plot_factor_bars(factor_stats: pd.DataFrame, path: Path) -> Path:
    """STUB-quality: annualised overnight vs intraday excess return per factor."""
    fig, ax = plt.subplots(figsize=(8, 4))
    factor_stats.plot.bar(ax=ax)
    ax.set_title("Factor ETFs minus SPY: overnight vs intraday (annualised)")
    return _save(fig, path)


def plot_strategies(results: list[StrategyResult], path: Path) -> Path:
    """STUB-quality: cumulative gross return per strategy."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for r in results:
        ax.plot(cumulative(r.gross), label=r.name)
    ax.set_title("Strategies: cumulative gross log return")
    ax.legend()
    return _save(fig, path)


def plot_costs(sweep: CostSweep, path: Path) -> Path:
    """STUB-quality: Sharpe vs cost per trade."""
    fig, ax = plt.subplots(figsize=(8, 4))
    sweep.sharpe.T.plot(ax=ax, marker="o")
    ax.set_xlabel("Cost per trade (bp)")
    ax.set_ylabel("Sharpe")
    ax.set_title("Sharpe after costs")
    return _save(fig, path)
