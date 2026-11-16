"""Regression tests for the findings of the final whole-branch review (C1, I1–I7)."""
import json
import textwrap

import numpy as np
import pandas as pd
import pytest
from conftest import make_ohlcv

from rekit.backtest import BacktestConfig, run_backtest
from rekit.cli import main
from rekit.lock import LockError, lock, verify_lock
from rekit.lookahead import LookAheadError, assert_no_lookahead
from rekit.paper import PaperTrader
from rekit.stats import bootstrap_ci
from rekit.verdict import Criteria, verdict


# C1 — an unlagged swing pivot must be caught every time, not with ~86 % probability
def unlagged_swing_failure(d: pd.DataFrame) -> pd.Series:
    pivot_hi = d.high.where(d.high == d.high.rolling(7, center=True).max()).ffill()
    return pd.Series(np.where((d.high > pivot_hi.shift(1)) & (d.close < pivot_hi.shift(1)), -1, 0), index=d.index)


@pytest.mark.parametrize("seed", range(30))
def test_c1_unlagged_swing_always_detected(seed):
    with pytest.raises(LookAheadError):
        assert_no_lookahead(unlagged_swing_failure, make_ohlcv(1500, seed=seed))


# I1 — gaps must stop a backtest unless the spec explicitly allows them
SPEC = '''
[defaults]
exchange = "bybit"
timeframe = "4h"
start = "2024-01-01"
end = "2025-06-01"
symbols = ["AAA"]
{extra}
[[hypothesis]]
id = "H1"
statement = "s"
rule = "rules.py:mom"
params = {{ n = 5 }}
[hypothesis.criteria]
min_trades = 10
'''
RULES = "import numpy as np\n\ndef mom(df, n=5):\n    return np.sign(df.close.diff(n)).fillna(0).astype(int)\n"


def project(tmp_path, extra="", gap=False):
    (tmp_path / "rules.py").write_text(RULES)
    d = tmp_path / "data"
    d.mkdir(exist_ok=True)
    df = make_ohlcv(1200, seed=2)
    if gap:
        df = df.drop(df.index[600])
    df.reset_index().to_csv(d / "AAA_4h.csv", index=False)
    spec = tmp_path / "h.toml"
    spec.write_text(textwrap.dedent(SPEC.format(extra=extra)))
    return spec, d


def test_i1_gap_stops_backtest(tmp_path, capsys):
    spec, d = project(tmp_path, gap=True)
    lock(spec)
    assert main(["backtest", str(spec), "--out", str(tmp_path / "o"), "--csv-dir", str(d)]) != 0
    assert "gap" in capsys.readouterr().err


def test_i1_gap_allowed_explicitly_is_recorded(tmp_path):
    spec, d = project(tmp_path, extra="allow_gaps = true", gap=True)
    lock(spec)
    assert main(["backtest", str(spec), "--out", str(tmp_path / "o"), "--csv-dir", str(d)]) == 0
    res = json.loads((tmp_path / "o" / "results.json").read_text())
    assert res["hypotheses"][0]["allow_gaps"] is True


# I2 — the lock covers the rule code too, and a lock is never silently replaced
def test_i2_rule_change_after_lock_is_refused(tmp_path):
    spec, _ = project(tmp_path)
    lock(spec)
    (tmp_path / "rules.py").write_text(RULES.replace("diff(n)", "diff(n + 1)"))
    with pytest.raises(LockError, match="rules.py"):
        verify_lock(spec)


def test_i2_relock_with_different_content_refused(tmp_path):
    spec, _ = project(tmp_path)
    lock(spec)
    spec.write_text(spec.read_text().replace("min_trades = 10", "min_trades = 11"))
    with pytest.raises(LockError, match="already locked"):
        lock(spec)


def test_i2_relock_same_content_is_noop(tmp_path):
    spec, _ = project(tmp_path)
    lock(spec)
    lock(spec)
    verify_lock(spec)


# I3 — correlated trades: block bootstrap must widen the interval and can flip ACCEPT
def clustered(seed=0, weeks=60, per_week=8):
    rng = np.random.default_rng(seed)
    week_effect = rng.normal(0.12, 1.0, weeks)
    values = np.repeat(week_effect, per_week) + rng.normal(0, 0.2, weeks * per_week)
    blocks = np.repeat(np.arange(weeks), per_week)
    return values, blocks


def test_i3_block_bootstrap_is_wider():
    v, b = clustered()
    lo, _, hi = bootstrap_ci(v)
    blo, _, bhi = bootstrap_ci(v, blocks=b)
    assert (bhi - blo) > 1.8 * (hi - lo)


def test_i3_verdict_uses_blocks():
    v, b = clustered(seed=3)
    naive = verdict(v, Criteria(min_trades=100), n_trials=1)
    blocked = verdict(v, Criteria(min_trades=100), n_trials=1, blocks=b)
    assert naive["verdict"] == "ACCEPT"
    assert blocked["verdict"] == "REJECT"


# I4 — concurrency is reported so a multi-symbol "total return" is not mistaken for a portfolio
def test_i4_summary_reports_concurrency(tmp_path):
    spec, d = project(tmp_path)
    (d / "BBB_4h.csv").write_text((d / "AAA_4h.csv").read_text())
    spec.write_text(spec.read_text().replace('symbols = ["AAA"]', 'symbols = ["AAA", "BBB"]'))
    lock(spec)
    assert main(["backtest", str(spec), "--out", str(tmp_path / "o"), "--csv-dir", str(d)]) == 0
    s = json.loads((tmp_path / "o" / "results.json").read_text())["hypotheses"][0]["summary"]
    assert s["max_concurrent_positions"] >= 2
    assert "exit-marked" in (tmp_path / "o" / "report.md").read_text()


# I5 — paper trading honours max_bars with a sliding window of fixed length
def test_i5_paper_time_exit_with_sliding_window(tmp_path):
    df = make_ohlcv(700, seed=4)
    rule = lambda d: np.sign(d.close.diff(5)).fillna(0).astype(int)  # noqa: E731
    cfg = BacktestConfig(max_bars=4, stop_atr=5, target_r=5)
    bt = run_backtest(df, rule(df), cfg).trades
    pt = PaperTrader(rule, cfg, tmp_path / "j.jsonl")
    for k in range(201, len(df) + 1):
        pt.on_bar(df.iloc[k - 200:k])   # always 200 bars, like the live poller
    closes = [json.loads(x) for x in (tmp_path / "j.jsonl").read_text().splitlines()]
    times = sum(1 for e in closes if e["event"] == "close" and e["exit_reason"] == "time")
    assert times > 10
    assert times == pytest.approx((bt[bt.entry_ts >= df.index[200]].exit_reason == "time").sum(), abs=2)


# I6 — the safety scanner catches camelCase, snake_case and dynamic imports
from test_safety import scan_text  # noqa: E402


@pytest.mark.parametrize("code", [
    "ex.createOrder('BTC', 'market', 'buy', 1)", "ex.cancelOrder(1)", "ex.fetchBalance()",
    "ex.private_post_v5_order_create({})", "ex.privatePostV5OrderCreate({})", '{"secret": "x"}',
    "c = __import__('ccxt')", "importlib.import_module('ccxt')", "ex.set_leverage(5)", "APIKEY = 'x'",
])
def test_i6_scanner_catches(code):
    assert scan_text(code), code


@pytest.mark.parametrize("text", ["handles API keys or secrets.", "fetch_ohlcv(symbol)", "withdrawn from the account"])
def test_i6_scanner_allows_prose(text):
    assert not scan_text(text), text


# I7 — with a grid, the baseline is judged on the same out-of-sample windows
def test_i7_grid_baseline_same_windows(tmp_path):
    spec, d = project(tmp_path)
    grid = 'grid = { n = [3, 8] }\nbaseline_rule = "rules.py:mom"\nbaseline_params = { n = 5 }'
    text = spec.read_text().replace("params = { n = 5 }", grid)
    spec.write_text(text.replace("[hypothesis.criteria]", '[hypothesis.criteria]\nmetric = "expectancy_diff_r"'))
    lock(spec)
    assert main(["backtest", str(spec), "--out", str(tmp_path / "o"), "--csv-dir", str(d)]) == 0
    h = json.loads((tmp_path / "o" / "results.json").read_text())["hypotheses"][0]
    assert h["baseline_window"] == "out-of-sample windows only"


def test_i3_weekly_sharpe_uses_weekly_result_not_average():
    # many small winning weeks with many trades, few weeks with a single small loss:
    # the weekly RESULT series is clearly positive; an average-per-week series would be dragged negative
    vals, blocks = [], []
    for w in range(200):
        if w % 5 == 0:
            vals += [-0.2]
            blocks += [w]
        else:
            vals += [0.05] * 10
            blocks += [w] * 10
    v = verdict(np.array(vals), Criteria(min_trades=100), n_trials=1, blocks=np.array(blocks))
    assert v["dsr_prob"] > 0.95
