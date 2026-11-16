import numpy as np
import pandas as pd
import pytest

from rekit.stats import bootstrap_ci, concentration, deflated_sharpe_prob, holm, min_trades


def test_bootstrap_deterministic_and_ordered():
    v = np.random.default_rng(3).normal(0.1, 1, 300)
    a, b = bootstrap_ci(v, seed=7), bootstrap_ci(v, seed=7)
    assert a == b
    lo, pt, hi = a
    assert lo <= pt <= hi
    assert pt == pytest.approx(v.mean())


def test_dsr_drops_with_more_trials():
    args = dict(sr=0.15, n_obs=300, skew=0.0, kurt=3.0, sr_trials_std=0.06)
    p1 = deflated_sharpe_prob(n_trials=1, **args)
    p50 = deflated_sharpe_prob(n_trials=50, **args)
    assert 0 <= p50 < p1 <= 1


def test_holm():
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])


def test_holm_caps_at_one():
    assert max(holm([0.6, 0.7])) <= 1.0


def test_min_trades():
    assert 150 <= min_trades(0.2, 1.0) <= 160


def test_concentration_top_trade_carries_everything():
    tr = pd.DataFrame({"r_multiple": [10, -1, -1, -1, -1], "symbol": list("abcde")})
    c = concentration(tr, top_k=1)
    assert c["top_share_pct"] > 100
    assert c["net_ex_top_r"] == pytest.approx(-4)
    assert c["expectancy_ex_top_r"] == pytest.approx(-1)


def test_concentration_by_symbol():
    tr = pd.DataFrame({"r_multiple": [3, 3, -1, -1], "symbol": ["a", "a", "b", "c"]})
    c = concentration(tr, top_k=1, by="symbol")
    assert c["top_share_pct"] == pytest.approx(150)
    assert c["net_ex_top_r"] == pytest.approx(-2)
