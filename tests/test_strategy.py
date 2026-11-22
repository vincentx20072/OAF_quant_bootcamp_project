"""Factor and strategy tests. Owner: Dev 3."""

import numpy as np
import pandas as pd
import pytest

from oi.contract import FACTOR_ETFS, MARKET, STRATEGY_NAMES, Prices, SplitReturns, StrategyResult
from oi.data import synthetic_prices
from oi.decompose import split_returns
from oi.factors import common_start, excess_split
from oi.metrics import annualised_stats
from oi.strategy import breakeven_bp, cost_sweep, net_stats, run_all

TICKERS = [MARKET] + list(FACTOR_ETFS.values())


@pytest.fixture(scope="module")
def prices() -> Prices:
    return synthetic_prices(start="2015-01-01", end="2018-12-31")


@pytest.fixture(scope="module")
def split(prices) -> SplitReturns:
    return split_returns(prices)


@pytest.fixture(scope="module")
def excess(prices, split) -> SplitReturns:
    return excess_split(split, common_start(prices))


@pytest.fixture(scope="module")
def results(excess):
    return {r.name: r for r in run_all(excess)}


# --------------------------------------------------------------------------- factors


def test_excess_columns_are_factor_names(excess):
    assert excess.columns == list(FACTOR_ETFS)


def test_excess_is_etf_minus_market(split, excess):
    for factor, etf in FACTOR_ETFS.items():
        idx = excess.overnight.index
        np.testing.assert_allclose(
            excess.overnight[factor], split.overnight.loc[idx, etf] - split.overnight.loc[idx, MARKET]
        )
        np.testing.assert_allclose(
            excess.intraday[factor], split.intraday.loc[idx, etf] - split.intraday.loc[idx, MARKET]
        )


def test_common_start_and_no_gaps_with_late_listing():
    """An ETF that lists late sets the common start; the excess frame has no NaN."""
    p = synthetic_prices(tickers=TICKERS, start="2012-01-02", end="2014-12-31")
    late = pd.Timestamp("2013-04-18")
    o, c = p.open.copy(), p.close.copy()
    o.loc[o.index < late, "MTUM"] = np.nan
    c.loc[c.index < late, "MTUM"] = np.nan
    p = Prices(o, c)
    start = common_start(p)
    assert start == late
    ex = excess_split(split_returns(p), start)
    assert ex.overnight.index[0] > late  # first MTUM overnight return needs a previous close
    assert not ex.overnight.isna().any().any()
    assert not ex.intraday.isna().any().any()


def test_excess_removes_market_drift():
    """Same drift in every ticker -> excess returns have (close to) zero mean."""
    p = synthetic_prices(tickers=TICKERS, start="2010-01-01", end="2024-12-31", seed=3)
    ex = excess_split(split_returns(p))
    assert abs(ex.overnight.mean().mean()) < 2e-4
    assert abs(ex.intraday.mean().mean()) < 2e-4


# --------------------------------------------------------------------------- strategies


def test_run_all_returns_four_named_strategies(results):
    assert list(results) == list(STRATEGY_NAMES)
    assert {n: r.trades_per_day for n, r in results.items()} == {
        "all_day_blend": 0.0, "overnight_leg": 2.0, "intraday_leg": 2.0, "switching": 2.0,
    }


def test_strategy_returns_match_definitions(excess, results):
    mom_on = excess.overnight["momentum"]
    others_intra = excess.intraday[["value", "low_vol", "quality", "size"]].mean(axis=1)
    np.testing.assert_allclose(results["overnight_leg"].gross, mom_on)
    np.testing.assert_allclose(results["intraday_leg"].gross, others_intra)
    np.testing.assert_allclose(results["switching"].gross, mom_on + others_intra)
    np.testing.assert_allclose(results["all_day_blend"].gross, excess.daily.mean(axis=1))


def test_switching_is_sum_of_legs(results):
    total = results["overnight_leg"].gross + results["intraday_leg"].gross
    np.testing.assert_allclose(results["switching"].gross, total)


def test_strategies_share_index(excess, results):
    for r in results.values():
        assert r.gross.index.equals(excess.overnight.index)
        assert not r.gross.isna().any()


# --------------------------------------------------------------------------- costs


def test_net_subtracts_cost_per_trade():
    r = StrategyResult("x", pd.Series([0.001, 0.001]), trades_per_day=2.0)
    assert r.net(1.0).tolist() == pytest.approx([0.0008, 0.0008])


def test_breakeven_known_value():
    # mean 1 bp/day, 2 trades/day -> break-even 0.5 bp per trade
    rng = np.random.default_rng(0)
    g = pd.Series(1e-4 + 1e-3 * rng.standard_normal(1000))
    g = g - g.mean() + 1e-4
    r = StrategyResult("x", g, trades_per_day=2.0)
    assert breakeven_bp(r) == pytest.approx(0.5)
    assert annualised_stats(r.net(breakeven_bp(r)))["ann_mean"] == pytest.approx(0.0, abs=1e-12)


def test_breakeven_nan_when_no_trades():
    r = StrategyResult("x", pd.Series([0.001, 0.002]), trades_per_day=0.0)
    assert np.isnan(breakeven_bp(r))


def test_cost_sweep_shape_and_monotone(results):
    sweep = cost_sweep(list(results.values()))
    assert list(sweep.sharpe.index) == list(STRATEGY_NAMES)
    assert list(sweep.sharpe.columns) == [0.0, 1.0, 2.0, 5.0]
    assert not sweep.sharpe.isna().any().any()
    # no trades -> costs don't matter
    assert sweep.sharpe.loc["all_day_blend"].nunique() == 1
    # trading strategies get strictly worse as costs rise
    for name in ("overnight_leg", "intraday_leg", "switching"):
        assert sweep.sharpe.loc[name].is_monotonic_decreasing
        assert sweep.sharpe.loc[name, 0.0] > sweep.sharpe.loc[name, 5.0]
    assert set(sweep.breakeven_bp) == set(STRATEGY_NAMES)
    assert np.isnan(sweep.breakeven_bp["all_day_blend"])


def test_cost_sweep_zero_cost_equals_gross(results):
    sweep = cost_sweep(list(results.values()))
    for name, r in results.items():
        assert sweep.sharpe.loc[name, 0.0] == pytest.approx(annualised_stats(r.gross)["sharpe"])


def test_net_stats_keys(results):
    ns = net_stats(list(results.values()))
    assert set(ns) == set(STRATEGY_NAMES)
    assert set(ns["switching"]) == {0.0, 1.0, 2.0, 5.0}
