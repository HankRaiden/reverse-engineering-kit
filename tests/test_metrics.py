import numpy as np
import pandas as pd
import pytest

from rekit.backtest import BacktestConfig, BacktestResult
from rekit.metrics import max_drawdown_pct, summarize


def result_from_r(rs, risk=1.0):
    idx = pd.date_range("2024-01-01", periods=len(rs), freq="1D", tz="UTC", name="ts")
    tr = pd.DataFrame({"r_multiple": rs, "return_pct": np.array(rs) * risk, "exit_ts": idx, "symbol": "X"})
    eq = (1 + tr.return_pct / 100).cumprod()
    eq.index = idx
    return BacktestResult(trades=tr, equity=eq, config=BacktestConfig(risk_pct=risk))


def test_profit_factor_and_hit_rate():
    s = summarize(result_from_r([2, -1, 2, -1]))
    assert s["profit_factor"] == pytest.approx(2.0)
    assert s["hit_rate"] == pytest.approx(0.5)
    assert s["expectancy_r"] == pytest.approx(0.5)
    assert s["n_trades"] == 4


def test_max_drawdown():
    eq = pd.Series([1.0, 1.2, 0.9, 1.1])
    assert max_drawdown_pct(eq) == pytest.approx(-25.0)


def test_total_return_compounds():
    s = summarize(result_from_r([10, -5], risk=1.0))
    assert s["total_return_pct"] == pytest.approx((1.10 * 0.95 - 1) * 100)


def test_empty_result_is_safe():
    s = summarize(result_from_r([]))
    assert s["n_trades"] == 0
    assert np.isnan(s["profit_factor"])
