"""Look-ahead detector: change the future, the past must not move."""
from __future__ import annotations

from collections.abc import Callable

import numpy as np
import pandas as pd

Rule = Callable[[pd.DataFrame], pd.Series]


class LookAheadError(AssertionError):
    """A rule's signal at time t changed when only data after t was changed."""


def _perturb_after(df: pd.DataFrame, t: int, rng: np.random.Generator) -> pd.DataFrame:
    out = df.copy()
    n = len(df) - t - 1
    if n <= 0:
        return out
    factor = np.exp(np.cumsum(rng.normal(0, 0.03, n)))
    cols = ["open", "high", "low", "close"]
    out.iloc[t + 1 :, [out.columns.get_loc(c) for c in cols]] = df[cols].iloc[t + 1 :].to_numpy() * factor[:, None]
    vcol = out.columns.get_loc("volume")
    out.iloc[t + 1 :, vcol] = df.volume.iloc[t + 1 :].to_numpy() * rng.lognormal(0, 0.8, n)
    return out


def assert_no_lookahead(rule: Rule, df: pd.DataFrame, checkpoints: int = 25, seed: int = 0) -> None:
    """Raise LookAheadError if the signal up to bar t depends on any bar after t."""
    rng = np.random.default_rng(seed)
    base = rule(df)
    lo, hi = int(len(df) * 0.1), int(len(df) * 0.9)
    for t in sorted(rng.integers(lo, hi, size=checkpoints)):
        changed = rule(_perturb_after(df, int(t), rng))
        a, b = base.iloc[: t + 1], changed.iloc[: t + 1]
        diff = ~((a == b) | (a.isna() & b.isna()))
        if diff.any():
            first = a.index[diff.to_numpy()][0]
            raise LookAheadError(
                f"signal at {first} changed after altering only data after {df.index[t]} — "
                "the rule looks into the future"
            )
