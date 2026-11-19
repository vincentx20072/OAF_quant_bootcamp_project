"""Plot and pipeline smoke tests. Owner: Dev 4 (plots), Dev 1 (pipeline)."""

import json
import sys
from pathlib import Path

from oi.contract import RESULTS_KEYS
from oi.data import synthetic_prices
from oi.decompose import split_returns
from oi.plots import plot_cumulative

ROOT = Path(__file__).resolve().parents[1]


def test_plot_cumulative_writes_png(tmp_path):
    split = split_returns(synthetic_prices(tickers=["SPY"], start="2020-01-01", end="2020-12-31"))
    out = plot_cumulative(split, "SPY", tmp_path / "c.png")
    assert out.exists() and out.stat().st_size > 1000


def test_pipeline_synthetic(tmp_path):
    sys.path.insert(0, str(ROOT / "scripts"))
    import run_all

    run_all.main(["--synthetic", "--out", str(tmp_path)])
    results = json.loads((tmp_path / "results.json").read_text())
    assert tuple(results) == RESULTS_KEYS
    assert results["meta"]["synthetic"] is True
    assert len(list((tmp_path / "figures").glob("*.png"))) == 5
