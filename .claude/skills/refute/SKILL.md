---
name: refute
description: Stage 7 — the challenger attacks every backtest result with six mandatory questions and fills the refutation register; the CIO then gives the verdict. Use after /backtest.
---
Role: **Challenger** (`.claude/agents/challenger.md`), verdict by **CIO**. Class: ANALYSIS.

1. Run the challenger on `work/06-backtest/results.json` with the six questions of
   `templates/<lang>/refutation-register.md`.
2. Write `work/07-refutation.md`: every refuted or weakened hypothesis with test, result, why it sounded plausible,
   and the condition for reopening.
3. The CIO gives a verdict per hypothesis (ACCEPT / ACCEPT_WITH_CONDITIONS / HOLD / REJECT) with `/review`.
4. Next step: `/paper-plan`. End with the four lines from `AGENTS.md` §5.
