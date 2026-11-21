# PLAN — Overnight vs Intraday

> **Repo:** everything lives in one public repo, `vincentx20072/OAF_quant_bootcamp_project` (code at the root, plan in `plans/`, background notes in `docs/research/`).

Prepared 2026-11-19 14:00 Europe/London for the OAF Quant Bootcamp mini-project. Source documents: `Quant_Bootcamp_Mini-Project.pdf` (the brief, "QB" below) and the group's one-page brief "Mini-Project Brief: Overnight vs Intraday Returns" (the doc, "BRIEF" below).

> **Contradiction flagged.** QB asks for "One version of the idea, done properly" and "make one or two clear charts". BRIEF adds a momentum twist, a factor-ETF extension and a switching strategy. This plan resolves it by priority: **P0** (the overnight/intraday split) is the one idea and owns the two headline charts. **P1** (factor ETFs + switching strategy + costs) is the single extension. **P2** (hand-built momentum WML) is optional and is cut first if hours run short, because MTUM already covers momentum.

## 0. Hook

Anyone who holds an index fund assumes they earn the market's return while the market is open. We show that, for US stocks and ETFs over the last 10–15 years, most of the return arrived *overnight*, between the close and the next open. We then test whether you can trade it by holding momentum overnight and other factors intraday, and find where costs kill it.

Why it sticks: one chart, two lines, one going up and one going nowhere.

## 1. Brief alignment (the "track lock")

**Chosen track:** a market-anomaly study with a simple strategy test. Rejected alternatives: leveraged-ETF decay (too mechanical, little to discuss) and pre-FOMC drift (needs event dates; fewer data points).

| Requirement | Source | Exact wording | How we meet it | Deck slide |
|---|---|---|---|---|
| Relevant topic | QB p.1 | "Work on any short project of your group's choice relevant to quant finance" | Return decomposition + factor timing | 1 |
| Free data | QB p.1 | "Pick one question about markets you can actually answer with free data in ~20 hours." | yfinance daily Open/Close, `auto_adjust=True` | 2 |
| Universe size | QB p.1 | "10-50 stocks or ETFs, one market, a few years" | 35 US tickers (SPY, QQQ, 8 sector ETFs, 5 factor ETFs, 20 large-caps), 2010–2026 | 2 |
| One idea | QB p.1 | "One version of the idea, done properly" | P0 split is the idea; P1 is one extension; P2 optional | 3–5 |
| Charts | QB p.1 | "make one or two clear charts" | Headline: cumulative overnight vs intraday; second: strategy Sharpe gross vs net. Others go in backup slides | 4, 6 |
| Real-life caveat | QB p.1 | "A sentence on what would break it in real life" | Break-even cost per trade in bp | 6 |
| No look-ahead | QB p.2 | "Watch for look-ahead bias: only use information that was available at the time of each trade." | Momentum ranks use month-end data before the holding month; tests check this | 5 |
| Deck size | QB p.1 | "Build a short deck (around 5-8 slides) and present it in Week 8." | 6 slides + 2 backup | — |
| Headline numbers | QB p.2 | "one or two charts and a couple of headline numbers (return, volatility, Sharpe)" | `results.json` holds annualised mean, vol, Sharpe for every series | 4, 6 |

**Technical shortcuts** (most visible effect for least code):
- `yf.download(tickers, start=..., auto_adjust=True, group_by="column")` returns adjusted Open and Close for all tickers in one call.
- Log returns make the split exact: `overnight = log(O_t/C_{t-1})`, `intraday = log(C_t/O_t)`, and the two sum to the daily return, so cumulative charts are just `cumsum`.
- Factor ETFs (MTUM, VLUE, USMV, QUAL, IWM) replace hand-built factor portfolios.

## 2. Critical checkpoints

All times Europe/London, 24-hour.

| Time | What | Consequence if missed |
|---|---|---|
| Fri 2026-11-20 18:00 | Group roster sent to the committee (QB: "Form a group and tell the committee who's in it.") | "If you don't have one, you'll be put in one." |
| TBC | Possible progress check-in (QB: "We might run a session to check in on progress") [VERIFY] | Lose early feedback |
| Sun 2026-11-22 20:00 | **Internal: end-to-end loop**: real data → split → cumulative chart → `results.json` | Everything later slips |
| Fri 2026-11-27 20:00 | Internal: P1 analyses done (factor split, strategies, costs) | P1 cut to a backup slide |
| Sat 2026-11-28 18:00 | **Internal: feature freeze**; numbers final | Deck built on moving numbers |
| Sun 2026-11-29 20:00 | Internal: final charts exported to `outputs/figures/` | — |
| Mon 2026-11-30 20:00 | Internal: deck draft | — |
| Tue 2026-12-01 19:00 | Internal: timed rehearsal (≤ 5 min) | Over-run on the day |
| Wed 2026-12-02 12:00 | **Internal: deck sent to oxfordalphafund@gmail.com** | — |
| Wed 2026-12-02 23:59 | **HARD: deck due** (QB: "Send us your deck the day before you present so we can line up the session.") Time of day [VERIFY] | Not lined up for the session |
| Thu 2026-12-03 TBC | **HARD: presentation** (QB: "Presentations in Week 8 (date TBC)") Date assumed [VERIFY] | — |

**Mandatory deliverables, as stated:** "Short slide deck, ~5 min talk + a few questions"; "Build a short deck (around 5-8 slides)"; "Send us your deck the day before you present".

## 3. Hard rules and disqualifiers

1. "Work on any short project of your group's choice relevant to quant finance" (QB p.1).
2. "Should not take more than 20 man-hours" (QB p.1); "Effort cap: 20 man-hours per group, total" (QB p.1).
3. "Form a group and tell the committee who's in it. If you don't have one, you'll be put in one." (QB p.1).
4. "Pick one question about markets you can actually answer with free data in ~20 hours." (QB p.1).
5. "Do the analysis: get the data, test the idea, make one or two clear charts." (QB p.1).
6. "Build a short deck (around 5-8 slides) and present it in Week 8. Date to be confirmed." (QB p.1).
7. "Send us your deck the day before you present so we can line up the session." (QB p.1).
8. Scope: "10-50 stocks or ETFs, one market, a few years"; "One version of the idea, done properly"; "5-8 slides, ~5 minute talk"; "A sentence on what would break it in real life" (QB p.1 table).
9. "Watch for look-ahead bias: only use information that was available at the time of each trade." (QB p.2).
10. "A null result is fine. 'It didn't work, and here's why' is a good presentation." (QB p.2).
11. Suggested deck structure: "The question", "Data", "Method: the rule or model in plain English (one equation at most).", "Results: one or two charts and a couple of headline numbers (return, volatility, Sharpe).", "Caveats and next steps" (QB p.2).
12. "Budget your hours: roughly a quarter on data, half on analysis, a quarter on the deck." (QB p.2).
13. No judging criteria, weights, banned tech or repo-visibility rules are stated in QB.

## 4. Architecture

**Pipeline (the user loop):**
1. `data.load_prices()` downloads adjusted Open/Close for the universe and caches them in `data/cache/`.
2. `decompose.split_returns()` turns prices into overnight, intraday and daily log returns.
3. `metrics.summary()` gives annualised mean, volatility and Sharpe; `decompose.gap_by_year()` gives the yearly overnight-minus-intraday gap.
4. `factors.excess_split()` subtracts SPY from each factor ETF, per half-day, from the common start date.
5. `strategy.run_all()` builds the four strategies (all-day blend, overnight leg, intraday leg, switching); `strategy.cost_sweep()` nets 0/1/2/5 bp per trade and finds the break-even cost.
6. `plots.*` writes PNGs to `outputs/figures/`; `scripts/run_all.py` writes `outputs/results.json`.
7. The deck uses those figures and numbers only.

**Data flow:** `Prices` → `SplitReturns` → `StatsRow` tables / `StrategyResult` → figures + `results.json` (all types in `src/oi/contract.py`).

**External APIs:**

| API | Does | Env vars | Limits |
|---|---|---|---|
| yfinance (Yahoo Finance, unofficial) | Daily OHLC, adjusted | none | Unofficial; rate-limits and occasional schema changes [VERIFY current version] |

**Fallbacks:**
- Yahoo rate-limits or breaks → the local cache in `data/cache/` (git-ignored; the repo is public) keeps the pipeline running once downloaded; `--synthetic` mode runs everything on generated prices so code and tests never need the network.
- A factor ETF missing early history → the common window starts at the latest first-date across the five (expected ~2013) [VERIFY].

## 5. Team split

Only Vincent is confirmed; other seats are TBD. Four roles at ~5 hours each keep the 20 man-hour cap. With fewer people, merge Dev 2 into Dev 3.

| Role | Person | Owns | Deliverables | Depends on |
|---|---|---|---|---|
| Dev 1: lead, data and core | vincent | `src/oi/contract.py`, `src/oi/data.py`, `src/oi/decompose.py`, `src/oi/metrics.py`, `scripts/`, `tests/test_core.py`, `pyproject.toml` | Cache, split, stats, `run_all.py`, `results.json` | — |
| Dev 2: momentum (P2) | TBD | `src/oi/momentum.py`, `tests/test_momentum.py` | 12-1 WML daily returns, split | contract, decompose |
| Dev 3: factors and strategy | TBD | `src/oi/factors.py`, `src/oi/strategy.py`, `tests/test_strategy.py` | Factor excess split, 4 strategies, cost sweep, break-even | contract, decompose, metrics |
| Dev 4: charts, deck, presenting | TBD | `src/oi/plots.py`, `tests/test_plots.py`, `deck/` | All figures, deck, rehearsal, sending the deck | everything |

Rules: one owner per folder or file. `src/oi/contract.py` is owned by Dev 1 and changes only through an announced `CONTRACT` comment. Dev 4 owns the deck, the talk and sending it.

## 6. Timeline

| Block | Who | Done when … |
|---|---|---|
| Thu 19 Nov – Fri 20 Nov | Dev 1 | Scaffold merged; `python -m pytest -q` passes; roster sent to committee |
| Sat 21 – Sun 22 Nov | Dev 1 | `python scripts/run_all.py` on real data writes `outputs/figures/cumulative_split.png` and `outputs/results.json` |
| Mon 23 – Fri 27 Nov | Dev 2, Dev 3 | `results.json` has `factors`, `strategies`, `costs.breakeven_bp` (and `momentum` if P2 done); tests pass |
| Sat 28 Nov 18:00 | all | Freeze: tag `v1-numbers` on `develop` |
| Sun 29 Nov | Dev 4 | Five PNGs in `outputs/figures/` match `results.json` |
| Mon 30 Nov | Dev 4 | Deck draft with 6 slides shared |
| Tue 1 Dec | all | Rehearsal under 5:00 by stopwatch |
| Wed 2 Dec 12:00 | Dev 4 | Deck emailed; sent mail visible in the outbox |

## 7. Talk and deck (the "demo")

**20-second hook:** "If you'd owned the S&P 500 only while the market was *closed* since 2010, you'd have made most of its return. Owning it only while it was open made close to nothing. We checked whether you can trade that."

**Talk script (5 minutes):**
1. Hook + headline chart, 40 s.
2. Data: 35 tickers, yfinance, 2010–2026, adjusted prices, 30 s.
3. Method: the one equation (log return = overnight + intraday), 40 s.
4. Result: cumulative chart + mean/vol/Sharpe for each half; yearly gap, 60 s.
5. Extension: factor ETFs by time of day, then the switching strategy vs benchmarks, 60 s.
6. Can you trade it? Sharpe gross vs net; break-even cost in bp, 50 s.
7. Caveats + next steps, 20 s.

**Inputs to prepare:** frozen `results.json` and PNGs from the `v1-numbers` tag; no live code in the talk.

**Plan B:** a PDF export of the deck on a USB stick and in email, in case the room laptop fails.

**Deck outline:** the question; data; method; headline result; extension (factor timing); can you trade it; caveats and next steps. Backups: momentum WML split (if P2 done), weekend vs weeknight.

## 8. CLAUDE.md

```markdown
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
```

## 9. Setup handoff

```yaml
event:   {name: "OAF Quant Bootcamp mini-project", url: "https://oxfordalphafund.com/quant-pitch-day-decks", submission_url: "mailto:oxfordalphafund@gmail.com", timezone: "Europe/London"}
project: {name: "Overnight vs Intraday", slug: "overnight-intraday"}
deadlines:
  - {at: "2026-11-20T18:00", what: "Group roster sent to committee", hard: false}
  - {at: "2026-11-22T20:00", what: "End-to-end loop on real data", hard: false}
  - {at: "2026-11-27T20:00", what: "P1 analyses done", hard: false}
  - {at: "2026-11-28T18:00", what: "Feature freeze, tag v1-numbers", hard: false}
  - {at: "2026-11-29T20:00", what: "Final charts", hard: false}
  - {at: "2026-11-30T20:00", what: "Deck draft", hard: false}
  - {at: "2026-12-01T19:00", what: "Timed rehearsal", hard: false}
  - {at: "2026-12-02T12:00", what: "Deck emailed (internal)", hard: false}
  - {at: "2026-12-02T23:59", what: "Deck due to committee", hard: true}
  - {at: "2026-12-03T09:00", what: "Presentation (date and time TBC)", hard: true}
product_repo:
  mode: new
  upstream: null
  integration_branch: develop
  clean_submission: false
  must_be_public_by: null
stack:   {language: "python", framework: "pandas", package_manager: pip, install_cmd: "python -m pip install -e \".[dev]\"", dev_cmd: "python scripts/run_all.py --synthetic", build_cmd: "python -m compileall -q src scripts", test_cmd: "python -m pytest -q"}
env_vars: [OI_DATA_DIR, OI_START]
contract_file: "src/oi/contract.py"
rooms:
  - {name: "overnight-intraday",          purpose: "plan, task claims, START/COMMIT/PR/BLOCKED/DONE, CONTRACT"}
  - {name: "overnight-intraday-data",     purpose: "data quality, yfinance quirks, universe choices"}
  - {name: "overnight-intraday-analysis", purpose: "results, strategy and cost findings"}
  - {name: "overnight-intraday-deck",     purpose: "slides, charts, talk script"}
roles:
  - {id: dev1, title: "lead, data and core", person: "vincent", owns: [src/oi/contract.py, src/oi/data.py, src/oi/decompose.py, src/oi/metrics.py, scripts/, tests/test_core.py, pyproject.toml]}
  - {id: dev2, title: "momentum (P2)", person: "TBD", owns: [src/oi/momentum.py, tests/test_momentum.py]}
  - {id: dev3, title: "factors and strategy", person: "TBD", owns: [src/oi/factors.py, src/oi/strategy.py, tests/test_strategy.py]}
  - {id: dev4, title: "charts, deck, presenting", person: "TBD", owns: [src/oi/plots.py, tests/test_plots.py, deck/]}
hot_files: [src/oi/contract.py, pyproject.toml, scripts/run_all.py, NOTES.md]
tasks:
  - {id: T01, slug: scaffold, title: "Contract, module stubs, synthetic pipeline, tests", role: dev1, scope: ["**"], depends: [], done_when: "pip install -e .[dev] and python -m pytest -q pass; run_all.py --synthetic writes outputs/results.json"}
  - {id: T02, slug: data-loader, title: "yfinance download with auto_adjust, cache, data checks", role: dev1, scope: [src/oi/data.py, tests/test_core.py, data/cache/], depends: [T01], done_when: "load_prices() returns Prices for UNIVERSE from 2010; cache reloads offline; check_prices() reports gaps and zero/negative prices"}
  - {id: T03, slug: core-split, title: "Split, cumulative, equal-weight basket, gap by year, stats", role: dev1, scope: [src/oi/decompose.py, src/oi/metrics.py, tests/test_core.py], depends: [T01], done_when: "overnight+intraday equals daily to 1e-12; summary() gives mean/vol/sharpe per series; tests pass"}
  - {id: T04, slug: run-all-real, title: "Pipeline on real data, results.json and headline chart", role: dev1, scope: [scripts/run_all.py], depends: [T02, T03], done_when: "python scripts/run_all.py writes outputs/results.json and outputs/figures/cumulative_split.png from real data"}
  - {id: T05, slug: factor-split, title: "Factor ETF excess-over-SPY split from common start", role: dev3, scope: [src/oi/factors.py, tests/test_strategy.py], depends: [T03], done_when: "excess_split() returns overnight/intraday excess per factor ETF from common_start(); stats in results.json under factors"}
  - {id: T06, slug: strategies, title: "Four strategies: all-day, overnight leg, intraday leg, switching", role: dev3, scope: [src/oi/strategy.py, tests/test_strategy.py], depends: [T05], done_when: "run_all() returns 4 StrategyResult with daily gross returns and trades per day; switching trades 2/day; tests pass"}
  - {id: T07, slug: costs, title: "Cost sweep 0/1/2/5 bp and break-even cost", role: dev3, scope: [src/oi/strategy.py, tests/test_strategy.py], depends: [T06], done_when: "cost_sweep() gives Sharpe per strategy per cost; breakeven_bp() solves Sharpe=0 for switching; in results.json"}
  - {id: T08, slug: momentum-wml, title: "P2: 12-1 momentum WML on large-caps, split overnight/intraday", role: dev2, scope: [src/oi/momentum.py, tests/test_momentum.py], depends: [T03], done_when: "wml_split() returns SplitReturns for WML; a test proves ranks use only prior month-end data"}
  - {id: T09, slug: charts, title: "All figures from results and series", role: dev4, scope: [src/oi/plots.py, tests/test_plots.py], depends: [T04, T07], done_when: "five PNGs in outputs/figures/ with titles, units and source note; test_plots passes"}
  - {id: T10, slug: deck, title: "6-slide deck + 2 backup slides and speaker notes", role: dev4, scope: [deck/], depends: [T09], done_when: "deck/ has the exported PDF; every number matches results.json at tag v1-numbers"}
  - {id: T11, slug: rehearse-send, title: "Timed rehearsal and send the deck", role: dev4, scope: [deck/], depends: [T10], done_when: "rehearsal under 5:00; deck emailed by 2026-12-02 12:00"}
```

## 10. Open questions and [VERIFY] list

| Item | Ask whom |
|---|---|
| Presentation date and time (assumed Thu 3 Dec 2026) | OAF committee, oxfordalphafund@gmail.com |
| Deck deadline time on the day before (assumed 23:59) | OAF committee |
| Whether a progress check-in session will run, and when | OAF committee |
| Whether hours spent by AI agents count toward the 20 man-hour cap | OAF committee |
| Group roster and GitHub usernames | Vincent |
| Current yfinance version and whether `auto_adjust=True` adjusts Open as well as Close | yfinance docs / quick check in T02 |
| Factor ETF inception dates (expected around 2013) | Check in T05 from the data's first valid date |
| Lou, Polk & Skouras (2019) sample period, for the "rough out-of-sample" claim | Paper (JFE 2019) |
