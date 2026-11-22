"""Time-of-day factor strategies and costs. Owner: Dev 3 (tasks T06, T07).

The four strategies (names in contract.STRATEGY_NAMES), all built on factors.excess_split, so each
is long factor ETFs and short SPY (dollar-neutral). Baskets are equal-weight across factors.

- all_day_blend: equal-weight of all five factors, held day and night (trades_per_day = 0)
- overnight_leg: OVERNIGHT_FACTORS held overnight only, flat intraday (trades_per_day = 2)
- intraday_leg: INTRADAY_FACTORS held intraday only, flat overnight (trades_per_day = 2)
- switching: OVERNIGHT_FACTORS overnight, INTRADAY_FACTORS intraday (trades_per_day = 2)

Cost model (settled in plans/00-architecture.md): one "trade" is one switch of the whole portfolio,
charged ``cost_bp`` on the strategy's notional. A switch at the open and one at the close make 2
trades a day. Caveat for the deck: a long/short switch trades two legs, so if your per-leg cost is
c bp, the comparable figure here is roughly 2c for overnight_leg and intraday_leg. In switching
the SPY short stays on and only the long side rotates, so per-leg and per-trade cost are about equal.
"""

from __future__ import annotations

import pandas as pd

from .contract import (
    COST_BPS,
    INTRADAY_FACTORS,
    OVERNIGHT_FACTORS,
    STRATEGY_NAMES,
    CostSweep,
    SplitReturns,
    StrategyResult,
)
from .metrics import annualised_stats

TRADES_PER_DAY = {"all_day_blend": 0.0, "overnight_leg": 2.0, "intraday_leg": 2.0, "switching": 2.0}


def _basket(frame: pd.DataFrame, factors: list[str]) -> pd.Series:
    """Equal-weight basket (mean of log returns: daily-rebalanced approximation)."""
    return frame[factors].mean(axis=1)


def run_all(excess: SplitReturns) -> list[StrategyResult]:
    """Daily gross log returns for each strategy, in STRATEGY_NAMES order."""
    on_leg = _basket(excess.overnight, OVERNIGHT_FACTORS)
    intra_leg = _basket(excess.intraday, INTRADAY_FACTORS)
    gross = {
        "all_day_blend": _basket(excess.daily, list(excess.columns)),
        "overnight_leg": on_leg,
        "intraday_leg": intra_leg,
        "switching": on_leg + intra_leg,
    }
    return [StrategyResult(name, gross[name].rename(name), TRADES_PER_DAY[name]) for name in STRATEGY_NAMES]


def breakeven_bp(result: StrategyResult) -> float:
    """Cost per trade (bp) at which mean net daily return is zero (so net Sharpe is zero).

    mean(gross) - trades_per_day * c / 1e4 = 0  =>  c = mean(gross) * 1e4 / trades_per_day.
    NaN for strategies that never trade. Negative means the strategy loses money even before costs.
    """
    if result.trades_per_day <= 0:
        return float("nan")
    mean = float(result.gross.dropna().mean())
    return mean * 1e4 / result.trades_per_day


def cost_sweep(results: list[StrategyResult], cost_bps: tuple[float, ...] = COST_BPS) -> CostSweep:
    """Annualised Sharpe of net returns per strategy (rows) per cost in bp per trade (columns)."""
    sharpe = pd.DataFrame(
        [[annualised_stats(r.net(c))["sharpe"] for c in cost_bps] for r in results],
        index=[r.name for r in results],
        columns=list(cost_bps),
        dtype=float,
    )
    return CostSweep(sharpe=sharpe, breakeven_bp={r.name: breakeven_bp(r) for r in results})


def net_stats(results: list[StrategyResult], cost_bps: tuple[float, ...] = COST_BPS) -> dict:
    """{strategy: {cost_bp: StatsRow}} for net returns. Handy for the results table."""
    return {r.name: {c: annualised_stats(r.net(c)) for c in cost_bps} for r in results}

