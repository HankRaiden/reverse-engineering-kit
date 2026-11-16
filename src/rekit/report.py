"""Write results as JSON (for machines) and Markdown (for the chairman). Percent and R only."""
from __future__ import annotations

import json
import math
from pathlib import Path

LABELS = {
    "en": {"title": "Backtest report", "hyp": "Hypothesis", "verdict": "Verdict", "reason": "Why",
           "trades": "Trades", "hit": "Hit rate", "pf": "Profit factor", "exp": "Expectancy (R)",
           "ret": "Total return (%)", "dd": "Max drawdown (%)", "sharpe": "Sharpe (annual)",
           "ci": "95% confidence interval (R)", "dsr": "Deflated-Sharpe probability", "holm": "p (Holm-adjusted)",
           "conc": "Concentration", "metric": "Tested metric",
           "m_abs": "expectancy", "m_diff": "difference vs. baseline",
           "top": "Share of net result from top 3 trades (%)",
           "ex": "Net result without top 3 trades (R)", "note":
           "Verdicts follow criteria registered before the test. HOLD means: not enough trades to decide."},
    "de": {"title": "Backtest-Bericht", "hyp": "Hypothese", "verdict": "Urteil", "reason": "Begründung",
           "trades": "Trades", "hit": "Trefferquote", "pf": "Profit-Faktor", "exp": "Erwartungswert (R)",
           "ret": "Gesamtrendite (%)", "dd": "Max. Zwischenverlust (%)", "sharpe": "Sharpe (annualisiert)",
           "ci": "95-%-Konfidenzintervall (R)", "dsr": "Deflated-Sharpe-Wahrscheinlichkeit",
           "holm": "p (Holm-korrigiert)", "conc": "Konzentration", "metric": "Geprüfte Messgröße",
           "m_abs": "Erwartungswert", "m_diff": "Differenz zur Vergleichsregel",
           "top": "Anteil der besten 3 Trades am Netto-Ergebnis (%)",
           "ex": "Netto-Ergebnis ohne die besten 3 Trades (R)", "note":
           "Die Urteile folgen Kriterien, die vor dem Test festgelegt wurden. HOLD heißt: zu wenige Trades für eine "
           "Entscheidung."},
}


def _f(x, fmt="{:.2f}") -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "–"
    return fmt.format(x)


def write_report(results: dict, out_dir: Path, lang: str = "en") -> Path:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    L = LABELS[lang]
    meta = results.get("meta", {})
    lines = [f"# {L['title']}", "", f"_{L['note']}_", ""]
    if meta:
        lines += [" · ".join(f"{k}: {v}" for k, v in meta.items()), ""]
    lines += [f"| {L['hyp']} | {L['verdict']} | {L['metric']} | {L['ci']} | {L['trades']} | {L['hit']} | {L['pf']} | "
              f"{L['exp']} | {L['dd']} | {L['holm']} |", "|---|---|---|---|---|---|---|---|---|---|"]
    for h in results["hypotheses"]:
        s, v = h["summary"], h["verdict"]
        ci = v.get("ci", [None] * 3)
        metric = L["m_diff"] if h.get("metric") == "expectancy_diff_r" else L["m_abs"]
        hit = s["hit_rate"] * 100 if s["hit_rate"] == s["hit_rate"] else None
        lines.append(
            f"| {h['id']} | **{v['verdict']}** | {metric} {_f(ci[1], '{:+.3f}')} | "
            f"[{_f(ci[0], '{:+.3f}')}, {_f(ci[2], '{:+.3f}')}] | {s['n_trades']} | {_f(hit, '{:.0f} %')} | "
            f"{_f(s['profit_factor'])} | {_f(s['expectancy_r'], '{:+.3f}')} | {_f(s['max_drawdown_pct'], '{:.1f}')} | "
            f"{_f(v.get('p_holm'), '{:.3f}')} |")
    for h in results["hypotheses"]:
        s, v, c = h["summary"], h["verdict"], h.get("concentration", {})
        lines += ["", f"## {h['id']} — {h['statement']}", "", f"- **{L['verdict']}:** {v['verdict']}",
                  f"- **{L['reason']}:** {v['reason']}", f"- **{L['ret']}:** {_f(s['total_return_pct'], '{:+.1f}')}",
                  f"- **{L['sharpe']}:** {_f(s['sharpe_annual'])}", f"- **{L['dsr']}:** {_f(v.get('dsr_prob'))}"]
        if c:
            lines += [f"- **{L['conc']}:** {L['top']}: {_f(c.get('top_share_pct'), '{:.0f}')} · "
                      f"{L['ex']}: {_f(c.get('net_ex_top_r'), '{:+.1f}')}"]
    md = out_dir / "report.md"
    md.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return md
