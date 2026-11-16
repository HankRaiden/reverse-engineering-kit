import json
import textwrap

import numpy as np
import pandas as pd
import pytest
from conftest import make_ohlcv

from rekit.backtest import BacktestConfig, run_backtest
from rekit.cli import main
from rekit.lock import LockError, lock, verify_lock
from rekit.paper import PaperTrader
from rekit.spec import load_spec

RULES = '''
import numpy as np
import pandas as pd

def momentum(df, n=5):
    return np.sign(df.close.diff(n)).fillna(0).astype(int)

def flat(df):
    return pd.Series(0, index=df.index)
'''


def make_project(tmp_path, n=3000):
    (tmp_path / "rules.py").write_text(RULES)
    data = tmp_path / "data"
    data.mkdir()
    for i, sym in enumerate(["AAA", "BBB"]):
        make_ohlcv(n, seed=i).reset_index().to_csv(data / f"{sym}_4h.csv", index=False)
    spec = tmp_path / "hypotheses.toml"
    spec.write_text(textwrap.dedent('''
        [meta]
        source = "test"
        created = "2026-11-16"

        [defaults]
        exchange = "bybit"
        timeframe = "4h"
        start = "2024-01-01"
        end = "2025-06-01"
        symbols = ["AAA", "BBB"]

        [[hypothesis]]
        id = "H1"
        statement = "Momentum has positive expectancy"
        rule = "rules.py:momentum"
        params = { n = 5 }
        [hypothesis.criteria]
        min_trades = 50
        [hypothesis.backtest]
        risk_pct = 0.5

        [[hypothesis]]
        id = "H2"
        statement = "Momentum with grid, judged out of sample"
        rule = "rules.py:momentum"
        grid = { n = [3, 10] }
        [hypothesis.criteria]
        min_trades = 50
    '''))
    return spec, data


def test_load_spec_defaults_and_paths(tmp_path):
    spec, _ = make_project(tmp_path)
    hs = load_spec(spec)
    assert [h.id for h in hs] == ["H1", "H2"]
    assert hs[0].symbols == ["AAA", "BBB"] and hs[0].timeframe == "4h"
    assert hs[0].backtest == BacktestConfig(risk_pct=0.5)
    assert hs[0].criteria.min_trades == 50
    assert hs[1].n_variants == 2
    assert callable(hs[0].rule_fn)


def test_lock_and_verify(tmp_path):
    spec, _ = make_project(tmp_path)
    with pytest.raises(LockError, match="not locked"):
        verify_lock(spec)
    lock(spec)
    verify_lock(spec)
    spec.write_text(spec.read_text().replace("min_trades = 50", "min_trades = 5", 1))
    with pytest.raises(LockError, match="changed after it was locked"):
        verify_lock(spec)


def test_backtest_refuses_unlocked_spec(tmp_path, capsys):
    spec, data = make_project(tmp_path)
    assert main(["backtest", str(spec), "--out", str(tmp_path / "out"), "--csv-dir", str(data)]) != 0
    assert "not locked" in capsys.readouterr().err


def test_backtest_refuses_modified_after_lock(tmp_path, capsys):
    spec, data = make_project(tmp_path)
    lock(spec)
    spec.write_text(spec.read_text() + "\n# tweak\n")
    assert main(["backtest", str(spec), "--out", str(tmp_path / "out"), "--csv-dir", str(data)]) != 0
    assert "locked" in capsys.readouterr().err


def test_cli_backtest_end_to_end(tmp_path):
    spec, data = make_project(tmp_path)
    lock(spec)
    out = tmp_path / "out"
    assert main(["backtest", str(spec), "--out", str(out), "--csv-dir", str(data), "--lang", "de"]) == 0
    res = json.loads((out / "results.json").read_text())
    assert {h["id"] for h in res["hypotheses"]} == {"H1", "H2"}
    assert all(h["verdict"]["verdict"] in {"ACCEPT", "REJECT", "HOLD"} for h in res["hypotheses"])
    assert res["meta"]["n_trials"] == 3
    assert all("p_holm" in h["verdict"] for h in res["hypotheses"])
    assert "Urteil" in (out / "report.md").read_text()


def test_check_lookahead_cli_flags_bad_rule(tmp_path, capsys):
    spec, data = make_project(tmp_path)
    peek = "\ndef peek(df, n=1):\n    return np.sign(df.close.shift(-1) - df.close).fillna(0).astype(int)\n"
    (tmp_path / "rules.py").write_text(RULES + peek)
    s = spec.read_text().replace('rule = "rules.py:momentum"', 'rule = "rules.py:peek"', 1)
    spec.write_text(s)
    assert main(["check-lookahead", str(spec), "--csv-dir", str(data)]) != 0
    assert "future" in capsys.readouterr().err


def test_paper_matches_backtest(tmp_path):
    df = make_ohlcv(400, seed=3)
    rule = lambda d: np.sign(d.close.diff(5)).fillna(0).astype(int)  # noqa: E731
    cfg = BacktestConfig()
    bt = run_backtest(df, rule(df), cfg).trades
    bt = bt[bt.exit_reason != "end"].reset_index(drop=True)
    pt = PaperTrader(rule, cfg, tmp_path / "journal.jsonl")
    for k in range(2, len(df) + 1):
        pt.on_bar(df.iloc[:k])
        pt.on_bar(df.iloc[:k])  # repeated call for the same bar must be a no-op
    closes = [json.loads(x) for x in (tmp_path / "journal.jsonl").read_text().splitlines()]
    closes = [e for e in closes if e["event"] == "close"]
    assert len(closes) == len(bt)
    np.testing.assert_allclose([e["r_multiple"] for e in closes], bt.r_multiple)
    assert [pd.Timestamp(e["entry_ts"]) for e in closes] == list(bt.entry_ts)


def test_paper_journal_no_currency(tmp_path):
    df = make_ohlcv(200, seed=1)
    pt = PaperTrader(lambda d: pd.Series(1, index=d.index), BacktestConfig(), tmp_path / "j.jsonl")
    for k in range(2, len(df) + 1):
        pt.on_bar(df.iloc[:k])
    text = (tmp_path / "j.jsonl").read_text().lower()
    assert "usd" not in text and "eur" not in text and "$" not in text
