---
name: backtest
description: Stage 6 — run the pre-registered tests with `rekit` and report the verdicts exactly as they come out. Use after gate 2 and rekit lock.
---
Role: **CTO**. Class: ANALYSIS.

1. `uv run rekit backtest work/05-hypotheses.toml --out work/06-backtest --lang <de|en>`
   (it refuses unlocked or changed files and re-checks look-ahead).
2. Report per hypothesis: verdict, reason, trades, expectancy with confidence interval, max drawdown,
   Holm-adjusted p, concentration (top 3 share, result without top 3). Copy numbers from `results.json`; do not round
   them into something nicer.
3. Lead with the uncomfortable findings: REJECTs, HOLDs, concentration.
4. Next step: `/refute`. End with the four lines from `AGENTS.md` §5 and a pointer to `DISCLAIMER.md`.
