import pandas as pd
import pytest

from rekit.data import DataError, load_csv


def _write(tmp_path, df, name="d.csv"):
    p = tmp_path / name
    df.reset_index().to_csv(p, index=False)
    return p


def test_load_csv_roundtrip_sorted_utc(tmp_path, ohlcv):
    shuffled = ohlcv.sample(frac=1, random_state=1)
    out = load_csv(_write(tmp_path, shuffled))
    assert out.index.is_monotonic_increasing
    assert str(out.index.tz) == "UTC"
    assert out.index.name == "ts"
    assert list(out.columns) == ["open", "high", "low", "close", "volume"]
    pd.testing.assert_frame_equal(out, ohlcv, check_freq=False)


def test_load_csv_rejects_duplicates(tmp_path, ohlcv):
    dup = pd.concat([ohlcv, ohlcv.iloc[[5]]])
    with pytest.raises(DataError, match="duplicate"):
        load_csv(_write(tmp_path, dup))


def test_load_csv_rejects_nan(tmp_path, ohlcv):
    bad = ohlcv.copy()
    bad.iloc[10, 3] = float("nan")
    with pytest.raises(DataError, match="NaN"):
        load_csv(_write(tmp_path, bad))


def test_load_csv_rejects_gap(tmp_path, ohlcv):
    gap = ohlcv.drop(ohlcv.index[42])
    with pytest.raises(DataError, match=str(ohlcv.index[42].date())):
        load_csv(_write(tmp_path, gap))
    assert len(load_csv(_write(tmp_path, gap, "g.csv"), allow_gaps=True)) == len(ohlcv) - 1
