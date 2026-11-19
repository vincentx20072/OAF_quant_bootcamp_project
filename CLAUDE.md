Read `AGENTS.md` first. Follow the `team-hub` skill (board protocol) and the `challenge-rules` skill (hard rules, deadlines) in `.claude/skills/`.

# Project: Overnight vs Intraday (OAF Quant Bootcamp — mini-project)

## Core Concept
1. Download adjusted daily Open/Close for the universe with yfinance; cache to data/cache/.
2. Split each daily log return into overnight log(O_t/C_{t-1}) and intraday log(C_t/O_t).
3. Report annualised mean, volatility and Sharpe for each half; yearly overnight-minus-intraday gap.
4. Factor ETFs (MTUM, VLUE, USMV, QUAL, IWM) minus SPY, split the same way, from their common start.
5. Strategies: all-day blend; MTUM-SPY overnight only; other-four-SPY intraday only; switching (MTUM-SPY overnight, others-SPY intraday).
6. Costs: net of 0/1/2/5 bp per trade; break-even bp.
7. Write outputs/figures/*.png and outputs/results.json; the deck uses only these.

## Target Bounties (Do Not Deviate From Stack)
- Data: yfinance, `auto_adjust=True` (dividend-adjusted Open and Close). Never unadjusted prices.
- Returns: natural-log returns everywhere; annualise with 252 trading days; Sharpe = mean/std * sqrt(252), risk-free rate 0.
- Universe constants live in src/oi/contract.py only.
- Momentum (P2): 12-1 signal, month-end ranking, terciles, equal weight, one-month hold.
- Charts: matplotlib only.

## Tech Stack
Python 3.11+, pandas, numpy, matplotlib, yfinance, pytest. Package `oi` in src/ layout, installed with `pip install -e ".[dev]"`.

## Directory Structure & Ownership Boundaries
- src/oi/contract.py [Dev 1: lead] — shared types: Prices, SplitReturns, StatsRow, StrategyResult, CostSweep; constants MARKET, INDEX_ETFS, SECTOR_ETFS, FACTOR_ETFS, STOCKS, UNIVERSE, TRADING_DAYS, COST_BPS. Changes only via an announced CONTRACT comment.
- src/oi/data.py [Dev 1: lead] — load_prices(), synthetic_prices(), cache read/write.
- src/oi/decompose.py [Dev 1: lead] — split_returns(), cumulative(), gap_by_year(), equal_weight().
- src/oi/metrics.py [Dev 1: lead] — annualised_stats(), summary().
- src/oi/momentum.py [Dev 2: momentum] — momentum_signal(), wml_weights(), wml_split().
- src/oi/factors.py [Dev 3: factors & strategy] — common_start(), excess_split().
- src/oi/strategy.py [Dev 3: factors & strategy] — run_all(), cost_sweep(), breakeven_bp().
- src/oi/plots.py [Dev 4: charts & deck] — plot_cumulative(), plot_gap_by_year(), plot_factor_bars(), plot_strategies(), plot_costs().
- scripts/run_all.py [Dev 1: lead] — pipeline entry point; `--synthetic` for offline.
- tests/test_<module>.py — owned by the module's owner.
- deck/ [Dev 4] — deck exports and speaker notes.
- data/cache/ — cached prices; outputs/ — generated, gitignored.

## Environment Variables
None required. Optional: OI_DATA_DIR (cache folder), OI_START (YYYY-MM-DD). None are secret.

## Hard Rules
1. 20 man-hours total for the whole group; cut P2 first.
2. Free data only; 10–50 tickers; one market (US).
3. No look-ahead: signals use only data up to the previous close.
4. Deck 5–8 slides, ~5 minutes, sent the day before (Wed 2 Dec).
5. Every number in the deck comes from outputs/results.json at tag v1-numbers.

## Immediate Next Step
Scaffold: write src/oi/contract.py with complete types and constants, add working stubs for every module, scripts/run_all.py --synthetic producing results.json, tests for each module, README with install/run. `pip install -e ".[dev]"`, `python -m compileall -q src` and `python -m pytest -q` must pass.
