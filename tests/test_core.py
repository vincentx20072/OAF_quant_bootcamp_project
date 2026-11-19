"""Core tests. Owner: Dev 1."""

import numpy as np
import pandas as pd
import pytest

from oi.contract import UNIVERSE, Prices
from oi.data import synthetic_prices
from oi.decompose import equal_weight, gap_by_year, split_returns
from oi.metrics import annualised_stats, summary


@pytest.fixture(scope="module")
def prices() -> Prices:
    return synthetic_prices(start="2015-01-01", end="2019-12-31", seed=1)


def test_universe_size_within_brief():
    assert 10 <= len(UNIVERSE) <= 50
    assert len(UNIVERSE) == len(set(UNIVERSE))


def test_prices_validate(prices):
    prices.validate()


def test_split_sums_to_daily(prices):
    split = split_returns(prices)
    daily = np.log(prices.close / prices.close.shift(1)).iloc[1:]
    np.testing.assert_allclose(split.daily.values, daily.values, atol=1e-12)


def test_synthetic_has_overnight_premium(prices):
    split = split_returns(prices)
    assert split.overnight.mean().mean() > split.intraday.mean().mean()


def test_equal_weight_and_gap(prices):
    split = split_returns(prices)
    ew = equal_weight(split, ["SPY", "QQQ"])
    assert ew.columns == ["EW"]
    gap = gap_by_year(ew)
    assert list(gap.index) == [2015, 2016, 2017, 2018, 2019]


def test_annualised_stats_known_values():
    r = pd.Series([0.01, -0.01] * 50)
    s = annualised_stats(r)
    assert s["n_days"] == 100
    assert s["ann_mean"] == pytest.approx(0.0, abs=1e-12)
    assert s["ann_vol"] > 0


def test_summary_shape(prices):
    split = split_returns(prices).select(["SPY", "QQQ"])
    table = summary(split)
    assert len(table) == 6
    assert set(table.columns) == {"ann_mean", "ann_vol", "sharpe", "n_days"}
