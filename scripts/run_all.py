"""Pipeline entry point. Owner: Dev 1.

    python scripts/run_all.py              # real data (yfinance, cached in data/cache/)
    python scripts/run_all.py --synthetic  # offline, generated prices

Writes outputs/results.json and outputs/figures/*.png. The deck uses only these files.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from oi import plots  # noqa: E402
from oi.contract import MARKET, RESULTS_KEYS, STOCKS, SplitReturns, nan_to_none  # noqa: E402
from oi.data import load_prices, synthetic_prices  # noqa: E402
from oi.decompose import equal_weight, gap_by_year, split_returns  # noqa: E402
from oi.factors import common_start, excess_split  # noqa: E402
from oi.metrics import annualised_stats, summary  # noqa: E402
from oi.momentum import wml_split  # noqa: E402
from oi.strategy import cost_sweep, run_all  # noqa: E402


def stats_to_dict(table: pd.DataFrame) -> dict:
    out: dict = {}
    for (series, half), row in table.iterrows():
        out.setdefault(series, {})[half] = {k: (nan_to_none(v) if k != "n_days" else int(v)) for k, v in row.items()}
    return out


def main(argv: list[str] | None = None) -> dict:
    p = argparse.ArgumentParser()
    p.add_argument("--synthetic", action="store_true", help="use generated prices (no network)")
    p.add_argument("--refresh", action="store_true", help="re-download instead of using the cache")
    p.add_argument("--start", default=None)
    p.add_argument("--out", type=Path, default=ROOT / "outputs")
    args = p.parse_args(argv)

    prices = synthetic_prices() if args.synthetic else load_prices(start=args.start, refresh=args.refresh)
    split = split_returns(prices)

    # P0: headline series = market, QQQ, equal-weight large-caps
    ew = equal_weight(split, STOCKS, "EW_STOCKS")
    headline = SplitReturns(
        pd.concat([split.overnight[[MARKET, "QQQ"]], ew.overnight], axis=1),
        pd.concat([split.intraday[[MARKET, "QQQ"]], ew.intraday], axis=1),
    )
    split_stats = summary(headline)
    gap = gap_by_year(headline)

    # P1: factor ETFs minus SPY, strategies, costs
    start = common_start(prices)
    excess = excess_split(split, start)
    factor_stats = summary(excess)
    strategies = run_all(excess)
    sweep = cost_sweep(strategies)

    # P2: momentum WML
    wml = wml_split(prices, split)

    results = {
        "meta": {
            "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "synthetic": args.synthetic,
            "start": str(prices.close.index[0].date()),
            "end": str(prices.close.index[-1].date()),
            "tickers": prices.tickers,
            "factor_common_start": str(pd.Timestamp(start).date()),
        },
        "split_stats": stats_to_dict(split_stats),
        "gap_by_year": {str(y): {c: nan_to_none(v) for c, v in row.items()} for y, row in gap.iterrows()},
        "factors": stats_to_dict(factor_stats),
        "strategies": {r.name: {"trades_per_day": r.trades_per_day, "gross": annualised_stats(r.gross)} for r in strategies},
        "costs": {
            "sharpe": {name: {str(c): nan_to_none(v) for c, v in row.items()} for name, row in sweep.sharpe.iterrows()},
            "breakeven_bp": {k: nan_to_none(v) for k, v in sweep.breakeven_bp.items()},
        },
        "momentum": stats_to_dict(summary(wml)),
    }
    assert tuple(results) == RESULTS_KEYS

    if args.synthetic:
        plots.SOURCE_NOTE = "SYNTHETIC DATA: pipeline check only, not real results."
    figs = args.out / "figures"
    plots.plot_cumulative(headline, MARKET, figs / "cumulative_split.png")
    plots.plot_gap_by_year(gap, MARKET, figs / "gap_by_year.png")
    factor_bars = factor_stats["ann_mean"].unstack("half")[["overnight", "intraday"]]
    plots.plot_factor_bars(factor_bars, figs / "factor_bars.png")
    plots.plot_strategies(strategies, figs / "strategies.png")
    plots.plot_costs(sweep, figs / "costs.png")

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "results.json").write_text(json.dumps(results, indent=2, default=lambda o: nan_to_none(o)))
    print(f"wrote {args.out / 'results.json'} and {len(list(figs.glob('*.png')))} figures")
    return results


if __name__ == "__main__":
    main()
