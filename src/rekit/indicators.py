"""Causal indicators: every value at bar t uses only bars <= t."""
from __future__ import annotations

import pandas as pd


def ema(s: pd.Series, n: int) -> pd.Series:
    return s.ewm(span=n, adjust=False).mean()


def rolling_mean(s: pd.Series, n: int) -> pd.Series:
    return s.rolling(n).mean()


def atr(df: pd.DataFrame, n: int = 14) -> pd.Series:
    prev_close = df.close.shift(1)
    tr = pd.concat([df.high - df.low, (df.high - prev_close).abs(), (df.low - prev_close).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()


def _swing(price: pd.Series, left: int, right: int, kind: str) -> pd.Series:
    window = left + right + 1
    roll = price.rolling(window).max() if kind == "high" else price.rolling(window).min()
    candidate = price.shift(right)  # the bar `right` bars ago is the pivot candidate
    # A pivot is only *known* once `right` further bars have closed, so the value appears late.
    return candidate.where(candidate == roll)


def swing_high(df: pd.DataFrame, left: int = 3, right: int = 3) -> pd.Series:
    """Confirmed swing high, reported `right` bars after the pivot bar (NaN elsewhere)."""
    return _swing(df.high, left, right, "high")


def swing_low(df: pd.DataFrame, left: int = 3, right: int = 3) -> pd.Series:
    """Confirmed swing low, reported `right` bars after the pivot bar (NaN elsewhere)."""
    return _swing(df.low, left, right, "low")
