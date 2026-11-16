"""Stage 4 output: the codable rules of the worked example, as causal functions.

Every function: (df, **params) -> pd.Series of -1 / 0 / +1, using only candles up to the current one.
Parameters are the example's OWN choices (marked as assumptions in 03-rules.md), not taken from any bot.
"""
import numpy as np
import pandas as pd

from rekit.indicators import ema, swing_high, swing_low


def _prior_range(df: pd.DataFrame, lookback: int) -> tuple[pd.Series, pd.Series]:
    # highest high / lowest low of the PREVIOUS `lookback` candles (the current candle is excluded)
    return df.high.shift(1).rolling(lookback).max(), df.low.shift(1).rolling(lookback).min()


def breakout_no_volume(df: pd.DataFrame, lookback: int = 20) -> pd.Series:
    """R1 baseline: close outside the prior range, no volume condition."""
    hi, lo = _prior_range(df, lookback)
    sig = np.where(df.close > hi, 1, np.where(df.close < lo, -1, 0))
    return pd.Series(sig, index=df.index)


def volume_breakout(df: pd.DataFrame, lookback: int = 20, vol_mult: float = 1.5) -> pd.Series:
    """R1: a breakout only counts with volume above `vol_mult` x the prior average volume."""
    base = breakout_no_volume(df, lookback)
    vol_ok = df.volume > vol_mult * df.volume.shift(1).rolling(lookback).mean()
    return base.where(vol_ok, 0).astype(int)


def volume_breakout_trend(df: pd.DataFrame, lookback: int = 20, vol_mult: float = 1.5, ema_n: int = 200) -> pd.Series:
    """R3: R1, but only in the direction of the long-term trend (close vs. EMA)."""
    sig = volume_breakout(df, lookback, vol_mult)
    trend = np.sign(df.close - ema(df.close, ema_n))
    return sig.where(sig == trend, 0).astype(int)


def swing_failure(df: pd.DataFrame, left: int = 3, right: int = 3) -> pd.Series:
    """R2: price sweeps the last CONFIRMED swing high (low) and closes back inside -> short (long)."""
    last_hi = swing_high(df, left, right).ffill()
    last_lo = swing_low(df, left, right).ffill()
    short = (df.high > last_hi) & (df.close < last_hi)
    long_ = (df.low < last_lo) & (df.close > last_lo)
    sig = np.where(short & ~long_, -1, np.where(long_ & ~short, 1, 0))
    return pd.Series(sig, index=df.index)
