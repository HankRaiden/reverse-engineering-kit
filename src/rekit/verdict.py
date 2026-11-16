"""Pre-registered verdicts: ACCEPT, REJECT or HOLD — decided by rules written down before the test."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .stats import bootstrap_draws, deflated_sharpe_prob

N_BOOT = 1000


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


def _hold(n: int, reason: str) -> dict:
    return {"verdict": "HOLD", "reason": reason, "ci": [float("nan")] * 3, "dsr_prob": float("nan"),
            "p_value": float("nan"), "n": n}


def _block_results(v: np.ndarray, blocks: np.ndarray | None) -> np.ndarray:
    """Per-block result (sum of R) — e.g. the weekly result series. Without blocks: the trades themselves."""
    if blocks is None:
        return v
    b = np.asarray(blocks)
    return np.array([v[b == k].sum() for k in np.unique(b)])


def verdict(values_r: np.ndarray, criteria: Criteria, n_trials: int, baseline_r: np.ndarray | None = None,
            blocks: np.ndarray | None = None, baseline_blocks: np.ndarray | None = None) -> dict:
    """Judge one hypothesis.

    - HOLD: fewer trades than registered.
    - Expectancy hypotheses: ACCEPT needs the lower CI bound above the threshold AND a deflated-Sharpe probability
      >= dsr_min (corrects for the number of tried variants).
    - Difference hypotheses: ACCEPT needs the lower CI bound of the difference above the threshold.
    - Holm correction across hypotheses is applied afterwards by the caller (rekit backtest).
    With `blocks` (calendar week per trade) the bootstrap resamples whole weeks: correlated trades are not
    counted as independent evidence.
    """
    v = np.asarray(values_r, dtype=float)
    n = len(v)
    if n < criteria.min_trades:
        return _hold(n, f"only {n} trades, pre-registered minimum is {criteria.min_trades}")
    lo_q, hi_q = criteria.alpha / 2, 1 - criteria.alpha / 2
    if criteria.metric == "expectancy_diff_r":
        if baseline_r is None or len(baseline_r) < criteria.min_trades:
            return _hold(n, "baseline has too few trades")
        b = np.asarray(baseline_r, dtype=float)
        da = bootstrap_draws(v, np.mean, N_BOOT, 0, blocks)
        db = bootstrap_draws(b, np.mean, N_BOOT, 1, baseline_blocks)
        d = da - db
        point = float(v.mean() - b.mean())
        ci = (float(np.quantile(d, lo_q)), point, float(np.quantile(d, hi_q)))
        p = max(1 / N_BOOT, float((d <= criteria.threshold).mean()))
        dsr = float("nan")
        ok = ci[0] > criteria.threshold
        reason = (f"difference {point:+.3f} R, 95% CI [{ci[0]:+.3f}, {ci[2]:+.3f}]"
                  + ("" if ok else f" does not clear {criteria.threshold:+.2f}"))
    else:
        draws = bootstrap_draws(v, np.mean, N_BOOT, 0, blocks)
        ci = (float(np.quantile(draws, lo_q)), float(v.mean()), float(np.quantile(draws, hi_q)))
        p = max(1 / N_BOOT, float((draws <= criteria.threshold).mean()))
        unit = _block_results(v, blocks)
        sd = unit.std(ddof=1) if len(unit) > 1 else 0.0
        skew, kurt = _moments(unit) if sd > 0 else (0.0, 3.0)
        dsr = deflated_sharpe_prob(unit.mean() / sd if sd > 0 else 0.0, len(unit), n_trials, skew, kurt,
                                   1 / np.sqrt(len(unit)))
        ok = ci[0] > criteria.threshold and dsr >= criteria.dsr_min
        sign = "negative" if ci[2] < criteria.threshold else ("not shown" if not ok else "shown")
        reason = (f"expectancy {ci[1]:+.3f} R, 95% CI [{ci[0]:+.3f}, {ci[2]:+.3f}] ({sign}), "
                  f"deflated-Sharpe probability {dsr:.2f} over {n_trials} tried variants")
    return {"verdict": "ACCEPT" if ok else "REJECT", "reason": reason, "ci": list(ci), "dsr_prob": dsr,
            "p_value": p, "n": n, "resampled": "by week" if blocks is not None else "by trade"}
