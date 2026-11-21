# Overnight vs Intraday

OAF Quant Bootcamp mini-project. Where does the US stock market earn its return: overnight (close → open) or intraday (open → close)? And can you trade it by holding momentum overnight and other factors intraday?

Full plan and pitch: `plans/PLAN.md`. Settled method choices: `plans/00-architecture.md`. Background notes: `docs/research/`.

## Install

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: py -m venv .venv ; .venv\Scripts\activate
python -m pip install -e ".[dev]"
```

## Run

```bash
python scripts/run_all.py --synthetic   # offline, generated prices (pipeline check only)
python scripts/run_all.py               # real data from yfinance, cached in data/cache/ (git-ignored)
python -m pytest -q                     # tests (offline)
```

Outputs: `outputs/results.json` and `outputs/figures/*.png`. Every number in the deck comes from these.

## Method

Log returns, so the two halves add up exactly:

    ln(C_t / C_{t-1}) = ln(O_t / C_{t-1}) + ln(C_t / O_t)
                         overnight          intraday

Prices are dividend-adjusted (`auto_adjust=True`), because the ex-dividend drop happens at the open.

## Code layout

| Path | Owner | What |
|---|---|---|
| `src/oi/contract.py` | Dev 1 | Shared types and constants. Change only via a CONTRACT comment. |
| `src/oi/data.py` | Dev 1 | yfinance download, cache, synthetic prices |
| `src/oi/decompose.py` | Dev 1 | Overnight/intraday split, baskets, gap by year |
| `src/oi/metrics.py` | Dev 1 | Annualised mean, vol, Sharpe |
| `src/oi/momentum.py` | Dev 2 | P2: 12-1 momentum WML |
| `src/oi/factors.py` | Dev 3 | Factor ETFs minus SPY |
| `src/oi/strategy.py` | Dev 3 | Four strategies, cost sweep, break-even |
| `src/oi/plots.py` | Dev 4 | Figures |
| `scripts/run_all.py` | Dev 1 | Pipeline |
| `deck/` | Dev 4 | Deck exports, speaker notes |
