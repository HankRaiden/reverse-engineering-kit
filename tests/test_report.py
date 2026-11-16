import json
import re

from rekit.report import write_report

RESULTS = {
    "meta": {"source": "demo", "n_trials": 2, "created": "2026-11-16"},
    "hypotheses": [{
        "id": "H1", "statement": "Volume breakout has positive expectancy", "symbols": ["BTC/USDT:USDT"],
        "summary": {"n_trades": 120, "hit_rate": 0.41, "profit_factor": 1.1, "expectancy_r": 0.05,
                    "total_return_pct": 4.2, "max_drawdown_pct": -9.5, "sharpe_annual": 0.4},
        "verdict": {"verdict": "REJECT", "reason": "CI includes 0", "ci": [-0.1, 0.05, 0.2], "dsr_prob": 0.6,
                    "p_value": 0.2, "p_holm": 0.4},
        "concentration": {"top_share_pct": 180.0, "net_r": 6.0, "net_ex_top_r": -4.8, "expectancy_ex_top_r": -0.04},
    }],
}


def test_report_writes_json_and_md(tmp_path):
    md = write_report(RESULTS, tmp_path, lang="en")
    assert md.name == "report.md"
    assert json.loads((tmp_path / "results.json").read_text())["hypotheses"][0]["id"] == "H1"
    text = md.read_text()
    assert "REJECT" in text and "H1" in text


def test_report_has_no_currency(tmp_path):
    text = write_report(RESULTS, tmp_path, lang="en").read_text()
    assert not re.search(r"\$|€|\bUSD\b|\bEUR\b|\d\s?USDT", text)


def test_report_german_labels(tmp_path):
    text = write_report(RESULTS, tmp_path, lang="de").read_text()
    assert "Urteil" in text and "Trefferquote" in text and "Erwartungswert" in text


def test_report_names_the_tested_metric_per_row(tmp_path):
    res = json.loads(json.dumps(RESULTS))
    diff = json.loads(json.dumps(RESULTS["hypotheses"][0]))
    diff.update(id="H2", metric="expectancy_diff_r")
    res["hypotheses"].append(diff)
    text = write_report(res, tmp_path, lang="en").read_text()
    row = next(line for line in text.splitlines() if line.startswith("| H2 "))
    assert "difference vs. baseline" in row
    text_de = write_report(res, tmp_path, lang="de").read_text()
    assert "Differenz zur Vergleichsregel" in next(x for x in text_de.splitlines() if x.startswith("| H2 "))
