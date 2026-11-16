import json
from pathlib import Path

import pytest
from conftest import make_ohlcv

from rekit.lock import verify_lock
from rekit.lookahead import assert_no_lookahead
from rekit.spec import load_spec

EX = Path(__file__).resolve().parents[1] / "examples" / "beispiel-emperorbtc-oeffentlich"
SPEC = EX / "work" / "05-hypotheses.toml"


def test_example_spec_is_locked():
    verify_lock(SPEC)


@pytest.mark.parametrize("h", load_spec(SPEC) if SPEC.exists() else [], ids=lambda h: h.id)
def test_example_rules_are_causal(h):
    df = make_ohlcv(800, seed=11)
    assert_no_lookahead(lambda d: h.rule_fn(d, **h.params), df)
    if h.baseline_fn:
        assert_no_lookahead(lambda d: h.baseline_fn(d, **h.baseline_params), df)


def test_example_results_have_verdicts_in_both_languages():
    for lang in ("en", "de"):
        res = json.loads((EX / "work" / "06-backtest" / lang / "results.json").read_text())
        ids = {h.id for h in load_spec(SPEC)}
        assert {h["id"] for h in res["hypotheses"]} == ids
        assert all(h["verdict"]["verdict"] in {"ACCEPT", "REJECT", "HOLD"} for h in res["hypotheses"])


def test_example_has_all_stage_files():
    for f in ["01-source.md", "02-principles", "03-rules.md", "04-codability.md", "05-hypotheses.md",
              "07-refutation.md", "08-paper-plan.md", "approval-log.jsonl", "rules.py"]:
        assert (EX / "work" / f).exists(), f
