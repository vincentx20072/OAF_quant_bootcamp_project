---
name: challenge-rules
description: Hard rules, deadlines, scope, ownership and exact method choices for the OAF Quant Bootcamp overnight-vs-intraday mini-project. Use before planning work, before changing method or scope, before touching the deck, and whenever a number, convention or deadline matters.
---

# Challenge rules: OAF Quant Bootcamp mini-project

## What we are building (PLAN §0)
Most US stock-market return over 2010–2026 arrived overnight (close → open), not intraday. P0: show it with one chart. P1: test holding momentum overnight and other factors intraday, and find the cost at which it stops working. P2 (optional, cut first): hand-built 12-1 momentum WML.

## Hard rules (verbatim from the brief, QB)
1. "Work on any short project of your group's choice relevant to quant finance"
2. "Should not take more than 20 man-hours" — "Effort cap: 20 man-hours per group, total"
3. "Form a group and tell the committee who's in it. If you don't have one, you'll be put in one."
4. "Pick one question about markets you can actually answer with free data in ~20 hours."
5. "Do the analysis: get the data, test the idea, make one or two clear charts."
6. "Build a short deck (around 5-8 slides) and present it in Week 8. Date to be confirmed."
7. "Send us your deck the day before you present so we can line up the session."
8. Scope: "10-50 stocks or ETFs, one market, a few years"; "One version of the idea, done properly"; "5-8 slides, ~5 minute talk"; "A sentence on what would break it in real life"
9. "Watch for look-ahead bias: only use information that was available at the time of each trade."
10. "A null result is fine. 'It didn't work, and here's why' is a good presentation."
11. Deck: "The question" / "Data" / "Method: the rule or model in plain English (one equation at most)." / "Results: one or two charts and a couple of headline numbers (return, volatility, Sharpe)." / "Caveats and next steps"
12. "Budget your hours: roughly a quarter on data, half on analysis, a quarter on the deck."
No judging weights, banned tech or repo-visibility rules are stated.

## Requirement → how we meet it

| Requirement | How |
|---|---|
| Free data | yfinance, `auto_adjust=True` |
| 10–50 tickers, one market | 35 US tickers in `contract.UNIVERSE` (test enforces 10–50) |
| One idea, 1–2 charts | P0 cumulative split chart + P1 strategy-after-costs chart; everything else is backup |
| Real-life caveat | break-even cost per trade (bp) for the switching strategy |
| No look-ahead | momentum ranks use only month-end closes before the holding month (T08 test) |

## Deadlines (Europe/London)

| When | What |
|---|---|
| Fri 20 Nov 18:00 | Roster to committee |
| Sun 22 Nov 20:00 | Internal: end-to-end loop on real data |
| Fri 27 Nov 20:00 | Internal: P1 done |
| **Sat 28 Nov 18:00** | **Feature freeze, tag `v1-numbers`** |
| Sun 29 Nov 20:00 | Final charts |
| Mon 30 Nov 20:00 | Deck draft |
| Tue 1 Dec 19:00 | Timed rehearsal ≤ 5:00 |
| Wed 2 Dec 12:00 | Deck emailed (internal) |
| **Wed 2 Dec 23:59** | **HARD: deck due** [VERIFY time] |
| **Thu 3 Dec TBC** | **HARD: presentation** [VERIFY date] |

## Ownership and contract
Contract file: `src/oi/contract.py` (Dev 1). Types: `Prices`, `SplitReturns`, `StatsRow`, `StrategyResult`, `CostSweep`. Constants: `UNIVERSE`, `FACTOR_ETFS`, `OVERNIGHT_FACTORS`, `INTRADAY_FACTORS`, `STRATEGY_NAMES`, `COST_BPS`, `RESULTS_KEYS`, `TRADING_DAYS`.

| Role | Owns |
|---|---|
| dev1 lead (vincent) | `contract.py`, `data.py`, `decompose.py`, `metrics.py`, `scripts/`, `tests/test_core.py`, `pyproject.toml` |
| dev2 momentum (TBD) | `momentum.py`, `tests/test_momentum.py` |
| dev3 factors & strategy (TBD) | `factors.py`, `strategy.py`, `tests/test_strategy.py` |
| dev4 charts & deck (TBD) | `plots.py`, `tests/test_plots.py`, `deck/` |

## Facts you will get wrong otherwise
- Log returns everywhere. overnight = ln(O_t/C_{t-1}), intraday = ln(C_t/O_t); they sum to the daily return exactly.
- Annualise with 252 days. Sharpe = annualised mean / annualised vol, risk-free 0.
- Prices must be adjusted: the ex-dividend drop happens at the open and would bias overnight returns down.
- Factor ETFs are long-only: always subtract SPY per half-day before comparing factors.
- Common window for factor ETFs starts at the latest first-valid date across MTUM, VLUE, USMV, QUAL, IWM, SPY (expected ~2013) [VERIFY].
- A "trade" = one switch of the whole portfolio; `StrategyResult.net(c)` subtracts `trades_per_day * c / 1e4` per day. Switching, overnight-only and intraday-only legs trade 2× per day; the all-day blend 0×.
- Break-even bp for a strategy = mean daily gross / (trades_per_day / 1e4).
- `--synthetic` output is fake. Never put synthetic numbers in the deck.
- [VERIFY] whether yfinance `auto_adjust=True` adjusts Open as well as Close in the current version (T02 checks).
- [VERIFY] Lou, Polk & Skouras (2019) sample period before claiming "out-of-sample".
- [VERIFY] whether agent hours count toward the 20 man-hour cap (ask the committee).

## How to test
`python -m pytest -q` (offline, synthetic). `python scripts/run_all.py --synthetic` must write `outputs/results.json` and 5 PNGs. Real run: `python scripts/run_all.py`.

## Submission checklist
- [ ] Every deck number traced to `outputs/results.json` at tag `v1-numbers`
- [ ] 5–8 slides; one equation at most; one or two main charts
- [ ] A slide on what breaks it in real life (break-even cost)
- [ ] Rehearsed under 5:00
- [ ] Emailed to oxfordalphafund@gmail.com by Wed 2 Dec 12:00; PDF on a USB stick as plan B
