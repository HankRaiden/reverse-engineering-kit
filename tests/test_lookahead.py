import numpy as np
import pandas as pd
import pytest

from rekit.indicators import ema
from rekit.lookahead import LookAheadError, assert_no_lookahead


def centered_rule(d: pd.DataFrame) -> pd.Series:
    return np.sign(d.close - d.close.rolling(5, center=True).mean()).fillna(0).astype(int)


def causal_rule(d: pd.DataFrame) -> pd.Series:
    fast, slow = ema(d.close, 10), ema(d.close, 30)
    return np.sign(fast - slow).fillna(0).astype(int)


def test_lookahead_detects_centered_rolling(ohlcv):
    with pytest.raises(LookAheadError):
        assert_no_lookahead(centered_rule, ohlcv)


def test_lookahead_passes_causal_rule(ohlcv):
    assert_no_lookahead(causal_rule, ohlcv)


def test_lookahead_detects_shift_minus_one(ohlcv):
    with pytest.raises(LookAheadError):
        assert_no_lookahead(lambda d: np.sign(d.close.shift(-1) - d.close).fillna(0).astype(int), ohlcv)
