import numpy as np

from rekit.indicators import atr, ema, rolling_mean, swing_high, swing_low


def test_ema_matches_pandas(ohlcv):
    np.testing.assert_allclose(ema(ohlcv.close, 10), ohlcv.close.ewm(span=10, adjust=False).mean())


def test_atr_positive(ohlcv):
    a = atr(ohlcv, 14)
    assert (a.dropna() > 0).all()
    assert a.iloc[:13].isna().all()


def test_rolling_mean_causal(ohlcv):
    rm = rolling_mean(ohlcv.volume, 5)
    assert np.isclose(rm.iloc[10], ohlcv.volume.iloc[6:11].mean())


def test_swing_high_is_confirmed_late(ohlcv):
    df = ohlcv.copy()
    i = 100
    df.iloc[i, df.columns.get_loc("high")] = df.high.max() * 2
    sh = swing_high(df, left=3, right=3)
    assert sh.iloc[i : i + 3].isna().all()
    assert sh.iloc[i + 3] == df.high.iloc[i]


def test_swing_low_is_confirmed_late(ohlcv):
    df = ohlcv.copy()
    i = 200
    df.iloc[i, df.columns.get_loc("low")] = df.low.min() / 2
    sl = swing_low(df, left=3, right=3)
    assert sl.iloc[i : i + 3].isna().all()
    assert sl.iloc[i + 3] == df.low.iloc[i]
