# Architecture (settled — do not re-decide)

Full plan: `plans/PLAN.md`. Tasks: `plans/tasks.json` (mirrored as issues on the board).

## Question
Where does the US market earn its return: overnight (close → open) or intraday (open → close)? Can a time-of-day factor switch beat holding the factors all day, after costs?

## Priorities
- **P0** split, stats, yearly gap, headline chart. Must ship.
- **P1** factor ETFs minus SPY by half-day; four strategies; cost sweep and break-even. The one extension.
- **P2** hand-built 12-1 momentum WML. Optional; cut first.

## Pipeline
`data.load_prices` → `decompose.split_returns` → `metrics.summary` / `decompose.gap_by_year` → `factors.excess_split` → `strategy.run_all` → `strategy.cost_sweep` → `plots.*` + `outputs/results.json` (written by `scripts/run_all.py`).

## Settled decisions
1. Data: yfinance daily, `auto_adjust=True`, 2010-01-01 to today, cached in `data/cache/*.csv.gz` (git-ignored: the repo is public, so each person downloads their own copy).
2. Universe: 35 tickers in `contract.UNIVERSE`: SPY, QQQ; XLK XLF XLE XLV XLI XLP XLY XLU; MTUM VLUE USMV QUAL IWM; 20 large-caps.
3. Returns: natural-log; overnight = ln(O_t/C_{t-1}); intraday = ln(C_t/O_t).
4. Stats: annualised with 252 days; Sharpe with risk-free 0.
5. Headline series: SPY, QQQ, equal-weight of the 20 large-caps (`EW_STOCKS`).
6. Factors: each ETF minus SPY, per half-day, from the common start date.
7. Strategies (`contract.STRATEGY_NAMES`): all_day_blend (5 factors, 0 trades/day), overnight_leg (momentum overnight only, 2), intraday_leg (other four intraday only, 2), switching (momentum overnight + other four intraday, 2).
8. Costs: 0, 1, 2, 5 bp per trade (whole-portfolio switch); break-even = mean daily gross / (trades_per_day / 1e4).
9. Momentum P2: 12-1 signal at month-end, terciles, equal weight, one-month hold.
10. Charts: matplotlib; deck numbers only from `results.json` at tag `v1-numbers`.

## Known caveats (go on the last slide)
- Two trades a day: spreads and opening-auction slippage.
- Survivorship bias in the 20 large-caps.
- Factor ETFs are long-only, rebalanced indices, not pure long-short factors.
- Hindsight: the overnight/intraday split comes from published research.
