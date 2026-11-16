import numpy as np

from rekit.verdict import Criteria, verdict


def test_hold_when_too_few_trades():
    v = verdict(np.ones(20), Criteria(min_trades=100), n_trials=1)
    assert v["verdict"] == "HOLD"
    assert "100" in v["reason"]


def test_accept_requires_ci_above_threshold():
    r = np.random.default_rng(1).normal(0.3, 1, 400)
    v = verdict(r, Criteria(min_trades=100), n_trials=1)
    assert v["verdict"] == "ACCEPT"
    assert v["ci"][0] > 0
    assert v["dsr_prob"] >= 0.95


def test_reject_noise():
    r = np.random.default_rng(2).normal(0.0, 1, 400)
    assert verdict(r, Criteria(min_trades=100), n_trials=1)["verdict"] == "REJECT"


def test_many_trials_can_flip_accept_to_reject():
    r = np.random.default_rng(6).normal(0.12, 1, 400)
    assert verdict(r, Criteria(min_trades=100), n_trials=1)["verdict"] == "ACCEPT"
    assert verdict(r, Criteria(min_trades=100), n_trials=500)["verdict"] == "REJECT"


def test_difference_against_baseline():
    rng = np.random.default_rng(4)
    better, base = rng.normal(0.5, 1, 400), rng.normal(0.0, 1, 400)
    v = verdict(better, Criteria(metric="expectancy_diff_r", min_trades=100), n_trials=1, baseline_r=base)
    assert v["verdict"] == "ACCEPT"
    same = verdict(base, Criteria(metric="expectancy_diff_r", min_trades=100), n_trials=1, baseline_r=base)
    assert same["verdict"] == "REJECT"
