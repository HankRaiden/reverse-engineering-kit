"""Statistics that protect against fooling yourself."""
from __future__ import annotations

from collections.abc import Callable
from statistics import NormalDist

import numpy as np
import pandas as pd

_N = NormalDist()


def bootstrap_draws(values: np.ndarray, stat: Callable[[np.ndarray], float] = np.mean, n: int = 1000,
                    seed: int = 0, blocks: np.ndarray | None = None) -> np.ndarray:
    """Bootstrap distribution of `stat`.

    Without `blocks` single trades are resampled. With `blocks` (e.g. the calendar week of each trade) whole blocks
    are resampled, which keeps trades that happened together together. Use blocks whenever trades are correlated —
    in crypto, trades on different coins in the same week usually are.
    """
    v = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    if blocks is None:
        return np.array([stat(v[rng.integers(0, len(v), len(v))]) for _ in range(n)])
    b = np.asarray(blocks)
    groups = [v[b == k] for k in np.unique(b)]
    return np.array([stat(np.concatenate([groups[i] for i in rng.integers(0, len(groups), len(groups))]))
                     for _ in range(n)])


def bootstrap_ci(values: np.ndarray, stat: Callable[[np.ndarray], float] = np.mean, n: int = 1000,
                 alpha: float = 0.05, seed: int = 0, blocks: np.ndarray | None = None) -> tuple[float, float, float]:
    """Percentile bootstrap: (low, point, high)."""
    v = np.asarray(values, dtype=float)
    if len(v) == 0:
        return (float("nan"),) * 3
    draws = bootstrap_draws(v, stat, n, seed, blocks)
    lo, hi = np.quantile(draws, [alpha / 2, 1 - alpha / 2])
    return float(lo), float(stat(v)), float(hi)


def deflated_sharpe_prob(sr: float, n_obs: int, n_trials: int, skew: float, kurt: float,
                         sr_trials_std: float) -> float:
    """Probability that the true Sharpe is above zero after trying `n_trials` variants.

    Bailey & López de Prado (2014). `sr` is per observation (per trade), not annualised;
    `kurt` is the plain (non-excess) kurtosis.
    """
    if n_obs < 2:
        return float("nan")
    if n_trials <= 1:
        sr0 = 0.0
    else:
        g = 0.5772156649
        sr0 = sr_trials_std * ((1 - g) * _N.inv_cdf(1 - 1 / n_trials) + g * _N.inv_cdf(1 - 1 / (n_trials * np.e)))
    denom = np.sqrt(max(1e-12, 1 - skew * sr + (kurt - 1) / 4 * sr**2))
    return float(_N.cdf((sr - sr0) * np.sqrt(n_obs - 1) / denom))


def holm(pvalues: list[float]) -> list[float]:
    """Holm-Bonferroni adjusted p-values, in the original order."""
    p = np.asarray(pvalues, dtype=float)
    m = len(p)
    order = np.argsort(p)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (m - rank) * p[i]))
        adj[i] = running
    return adj.tolist()


def min_trades(effect_r: float, sd_r: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Trades needed to detect a mean of `effect_r` (one-sided test) with the given power."""
    z = _N.inv_cdf(1 - alpha) + _N.inv_cdf(power)
    return int(np.ceil((z * sd_r / effect_r) ** 2))


def concentration(trades: pd.DataFrame, top_k: int = 3, by: str = "trade") -> dict:
    """How much of the result comes from the best `top_k` trades (or symbols) — and what is left without them."""
    if by == "symbol":
        groups = trades.groupby("symbol")["r_multiple"]
        per = groups.sum().sort_values(ascending=False)
        top = per.index[:top_k]
        rest = trades[~trades["symbol"].isin(top)]["r_multiple"]
        top_sum = per.iloc[:top_k].sum()
    else:
        r = trades["r_multiple"].sort_values(ascending=False)
        top_sum = r.iloc[:top_k].sum()
        rest = r.iloc[top_k:]
    net = trades["r_multiple"].sum()
    return {
        "top_share_pct": float(top_sum / net * 100) if net != 0 else float("nan"),
        "net_r": float(net),
        "net_ex_top_r": float(rest.sum()),
        "expectancy_ex_top_r": float(rest.mean()) if len(rest) else float("nan"),
    }
