"""Momentum tests. Owner: Dev 2. T08 adds a no-look-ahead test."""

from oi.contract import STOCKS
from oi.data import synthetic_prices
from oi.decompose import split_returns
from oi.momentum import momentum_signal, wml_split


def test_wml_split_shape():
    prices = synthetic_prices(tickers=STOCKS, start="2015-01-01", end="2017-12-31")
    split = split_returns(prices)
    wml = wml_split(prices, split)
    assert wml.columns == ["WML"]
    assert wml.overnight.index.equals(split.overnight.index)


def test_signal_is_month_end():
    prices = synthetic_prices(tickers=STOCKS, start="2015-01-01", end="2016-12-31")
    sig = momentum_signal(prices.close)
    assert list(sig.columns) == STOCKS
    assert (sig.index.is_month_end).all()
