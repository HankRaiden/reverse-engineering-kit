import numpy as np
import pandas as pd

from rekit.backtest import BacktestConfig
from rekit.walkforward import walk_forward


def trend_then_crash(n=600):
    """Rises for the first 70 %, falls afterwards."""
    k = int(n * 0.7)
    steps = np.r_[np.full(k, 0.004), np.full(n - k, -0.006)]
    close = 100 * np.exp(np.cumsum(steps + np.random.default_rng(0).normal(0, 0.002, n)))
    open_ = np.r_[close[0], close[:-1]]
    idx = pd.date_range("2024-01-01", periods=n, freq="4h", tz="UTC", name="ts")
    return pd.DataFrame({"open": open_, "high": np.maximum(open_, close) * 1.002,
                         "low": np.minimum(open_, close) * 0.998, "close": close, "volume": 1.0}, index=idx)


def const_side(side):
    return lambda d: pd.Series(side, index=d.index)


def test_walk_forward_params_chosen_in_sample_only():
    df = trend_then_crash()
    out = walk_forward(df, const_side, {"side": [1, -1]}, BacktestConfig(), n_splits=1, train_frac=0.7)
    assert out["chosen_params"] == [{"side": 1}]          # the past said "long"
    assert out["oos_summary"]["expectancy_r"] < 0         # the future punished it
    assert (out["oos_trades"].entry_ts >= df.index[int(len(df) * 0.7)]).all()


def test_walk_forward_reports_is_vs_oos():
    df = trend_then_crash()
    out = walk_forward(df, const_side, {"side": [1, -1]}, BacktestConfig(), n_splits=1, train_frac=0.7)
    is_e, oos_e = out["is_vs_oos_expectancy"][0]
    assert is_e > oos_e
