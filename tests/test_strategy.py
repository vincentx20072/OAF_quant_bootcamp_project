"""Factor and strategy tests. Owner: Dev 3."""

import pandas as pd
import pytest

from oi.contract import FACTOR_ETFS, STRATEGY_NAMES, StrategyResult
from oi.data import synthetic_prices
from oi.decompose import split_returns
from oi.factors import common_start, excess_split
from oi.strategy import cost_sweep, run_all


@pytest.fixture(scope="module")
def excess():
    prices = synthetic_prices(start="2015-01-01", end="2018-12-31")
    split = split_returns(prices)
    return excess_split(split, common_start(prices))


def test_excess_columns_are_factor_names(excess):
    assert excess.columns == list(FACTOR_ETFS)


def test_run_all_returns_four_named_strategies(excess):
    results = run_all(excess)
    assert [r.name for r in results] == list(STRATEGY_NAMES)
    assert {r.name: r.trades_per_day for r in results}["switching"] == 2.0


def test_net_subtracts_cost_per_trade():
    r = StrategyResult("x", pd.Series([0.001, 0.001]), trades_per_day=2.0)
    assert r.net(1.0).tolist() == pytest.approx([0.0008, 0.0008])


def test_cost_sweep_shape(excess):
    sweep = cost_sweep(run_all(excess))
    assert list(sweep.sharpe.index) == list(STRATEGY_NAMES)
    assert list(sweep.sharpe.columns) == [0.0, 1.0, 2.0, 5.0]
