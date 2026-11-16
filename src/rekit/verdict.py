"""Pre-registered verdicts: ACCEPT, REJECT or HOLD — decided by rules written down before the test."""
from __future__ import annotations

from dataclasses import dataclass
from statistics import NormalDist

import numpy as np

from .stats import bootstrap_ci, deflated_sharpe_prob

_N = NormalDist()


@dataclass(frozen=True)
class Criteria:
    metric: str = "expectancy_r"      # or "expectancy_diff_r" (needs a baseline)
    threshold: float = 0.0            # the lower confidence bound must clear this
    min_trades: int = 100             # below this: HOLD (not enough evidence either way)
    alpha: float = 0.05
    dsr_min: float = 0.95


def _moments(v: np.ndarray) -> tuple[float, float]:
    m, s = v.mean(), v.std(ddof=1)
    if s == 0:
        return 0.0, 3.0
    z = (v - m) / s
    return float((z**3).mean()), float((z**4).mean())


def _diff_ci(a: np.ndarray, b: np.ndarray, n: int = 1000, alpha: float = 0.05, seed: int = 0):
    rng = np.random.default_rng(seed)
    d = [a[rng.integers(0, len(a), len(a))].mean() - b[rng.integers(0, len(b), len(b))].mean() for _ in range(n)]
    lo, hi = np.quantile(d, [alpha / 2, 1 - alpha / 2])
    return float(lo), float(a.mean() - b.mean()), float(hi)


def verdict(values_r: np.ndarray, criteria: Criteria, n_trials: int, baseline_r: np.ndarray | None = None) -> dict:
    v = np.asarray(values_r, dtype=float)
    n = len(v)
    if n < criteria.min_trades:
        return {"verdict": "HOLD", "reason": f"only {n} trades, pre-registered minimum is {criteria.min_trades}",
                "ci": [float("nan")] * 3, "dsr_prob": float("nan"), "p_value": float("nan"), "n": n}
    if criteria.metric == "expectancy_diff_r":
        if baseline_r is None or len(baseline_r) < criteria.min_trades:
            return {"verdict": "HOLD", "reason": "baseline has too few trades", "ci": [float("nan")] * 3,
                    "dsr_prob": float("nan"), "p_value": float("nan"), "n": n}
        b = np.asarray(baseline_r, dtype=float)
        ci = _diff_ci(v, b, alpha=criteria.alpha)
        se = np.sqrt(v.var(ddof=1) / n + b.var(ddof=1) / len(b))
        p = 1 - _N.cdf(ci[1] / se) if se > 0 else float("nan")
        dsr = float("nan")
        ok = ci[0] > criteria.threshold
        reason = (f"difference {ci[1]:+.3f} R, 95% CI [{ci[0]:+.3f}, {ci[2]:+.3f}]"
                  + ("" if ok else f" does not clear {criteria.threshold:+.2f}"))
    else:
        ci = bootstrap_ci(v, alpha=criteria.alpha)
        sd = v.std(ddof=1)
        p = 1 - _N.cdf(v.mean() / (sd / np.sqrt(n))) if sd > 0 else float("nan")
        skew, kurt = _moments(v)
        dsr = deflated_sharpe_prob(v.mean() / sd if sd > 0 else 0.0, n, n_trials, skew, kurt, 1 / np.sqrt(n))
        ok = ci[0] > criteria.threshold and dsr >= criteria.dsr_min
        reason = (f"expectancy {ci[1]:+.3f} R, 95% CI [{ci[0]:+.3f}, {ci[2]:+.3f}], "
                  f"deflated-Sharpe probability {dsr:.2f} over {n_trials} tried variants")
    return {"verdict": "ACCEPT" if ok else "REJECT", "reason": reason, "ci": list(ci), "dsr_prob": dsr,
            "p_value": float(p), "n": n}
