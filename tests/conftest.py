import numpy as np
import pandas as pd
import pytest


def make_ohlcv(n: int = 500, seed: int = 0, freq: str = "4h") -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    close = 100 * np.exp(np.cumsum(rng.normal(0, 0.01, n)))
    open_ = np.concatenate([[close[0]], close[:-1]])
    spread = np.abs(rng.normal(0, 0.006, n)) * close
    high = np.maximum(open_, close) + spread
    low = np.minimum(open_, close) - spread
    volume = rng.lognormal(10, 0.4, n)
    idx = pd.date_range("2024-01-01", periods=n, freq=freq, tz="UTC", name="ts")
    return pd.DataFrame({"open": open_, "high": high, "low": low, "close": close, "volume": volume}, index=idx)


@pytest.fixture
def ohlcv() -> pd.DataFrame:
    return make_ohlcv()
