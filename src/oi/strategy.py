"""Time-of-day factor strategies and costs. Owner: Dev 3. Tasks T06 and T07 replace the stubs.

The four strategies (names in contract.STRATEGY_NAMES), all hedged with SPY via factors.excess_split:
- all_day_blend: equal-weight of all five factors, held all day and night (trades_per_day = 0)
- overnight_leg: OVERNIGHT_FACTORS held overnight only, flat intraday (trades_per_day = 2)
- intraday_leg: INTRADAY_FACTORS held intraday only, flat overnight (trades_per_day = 2)
- switching: OVERNIGHT_FACTORS overnight, INTRADAY_FACTORS intraday (trades_per_day = 2)
"""

from __future__ import annotations

import pandas as pd

from .contract import COST_BPS, STRATEGY_NAMES, CostSweep, SplitReturns, StrategyResult

TRADES_PER_DAY = {"all_day_blend": 0.0, "overnight_leg": 2.0, "intraday_leg": 2.0, "switching": 2.0}


def run_all(excess: SplitReturns) -> list[StrategyResult]:
    """STUB: zero returns for each strategy. T06 builds the real daily gross returns."""
    zeros = pd.Series(0.0, index=excess.overnight.index)
    return [StrategyResult(name, zeros.copy(), TRADES_PER_DAY[name]) for name in STRATEGY_NAMES]


def breakeven_bp(result: StrategyResult) -> float:
    """Cost per trade (bp) at which mean net return is zero. STUB: NaN. T07 implements."""
    return float("nan")


def cost_sweep(results: list[StrategyResult], cost_bps: tuple[float, ...] = COST_BPS) -> CostSweep:
    """STUB: NaN Sharpe table with the right shape. T07 fills it using metrics.annualised_stats(r.net(c))."""
    sharpe = pd.DataFrame(float("nan"), index=[r.name for r in results], columns=list(cost_bps))
    return CostSweep(sharpe=sharpe, breakeven_bp={r.name: breakeven_bp(r) for r in results})
