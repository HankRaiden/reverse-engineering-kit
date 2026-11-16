---
name: paper-plan
description: Stage 8 — plan paper trading (real prices, fictitious trades, never orders) with stop and success criteria fixed in advance, then stop at gate 3. Use after /refute.
---
Role: **CIO + CTO**. Class: DECISION (gate 3).

1. Fill `templates/<lang>/paper-plan.md` → `work/08-paper-plan.md`. If no hypothesis is ACCEPT, say clearly that no
   paper start is recommended, or that it would be for learning only.
2. Fix the stop and success criteria before starting; take the limits from the backtest confidence intervals.
3. Ask the chairman for: `CHAIRMAN-GO: paper start H<N> is approved.` Record it with `/chairman`.
4. Only then the CTO starts `uv run rekit paper work/05-hypotheses.toml --hypothesis H<N>`.
5. Weekly: `templates/<lang>/weekly-review.md`; every close: `templates/<lang>/post-mortem.md`.
6. There is no live stage. Point to `docs/<lang>/after-paper-trading.md` and `DISCLAIMER.md`.
