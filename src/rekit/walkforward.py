"""Walk-forward: choose parameters on the past, judge them only on the following, unseen period."""
from __future__ import annotations

import itertools
from collections.abc import Callable

import numpy as np
import pandas as pd

from .backtest import BacktestConfig, run_backtest
from .metrics import result_from_trades, summarize


def _grid(grid: dict[str, list]) -> list[dict]:
    keys = list(grid)
    return [dict(zip(keys, vals, strict=True)) for vals in itertools.product(*(grid[k] for k in keys))]


def _trades_between(df: pd.DataFrame, rule, cfg, start: int, end: int) -> pd.DataFrame:
    hist = df.iloc[:end]  # never hand the rule anything after `end`
    tr = run_backtest(hist, rule(hist), cfg).trades
    return tr[tr.entry_ts >= df.index[start]]


def walk_forward(df: pd.DataFrame, rule_factory: Callable[..., Callable], grid: dict[str, list],
                 cfg: BacktestConfig | None = None, n_splits: int = 4, train_frac: float = 0.7) -> dict:
    cfg = cfg or BacktestConfig()
    n = len(df)
    chosen, pairs, oos, windows = [], [], [], []
    for k in range(n_splits):
        s0, s1 = k * n // n_splits, (k + 1) * n // n_splits
        t_end = s0 + int((s1 - s0) * train_frac)
        best, best_e = None, -np.inf
        for params in _grid(grid):
            tr = _trades_between(df, rule_factory(**params), cfg, s0, t_end)
            e = tr.r_multiple.mean() if len(tr) else -np.inf
            if e > best_e:
                best, best_e = params, e
        chosen.append(best)
        test = _trades_between(df, rule_factory(**best), cfg, t_end, s1)
        oos.append(test)
        windows.append((df.index[t_end], df.index[s1 - 1]))
        pairs.append((float(best_e), float(test.r_multiple.mean()) if len(test) else float("nan")))
    oos_trades = pd.concat(oos, ignore_index=True) if oos else pd.DataFrame()
    return {"oos_trades": oos_trades, "chosen_params": chosen,
            "oos_summary": summarize(result_from_trades(oos_trades, cfg)), "is_vs_oos_expectancy": pairs,
            "oos_windows": windows}
