---
name: codability
description: Stage 4 — the CTO checks which rules can be coded, writes them as causal functions in work/rules.py and documents what is lost. Use after /rules.
---
Role: **CTO** (`.claude/agents/cto.md`). Class: ANALYSIS. Requires an assignment (`/assignment`).

1. For every rule in `work/03-rules.md` fill a row of `templates/<lang>/codability-matrix.md` →
   `work/04-codability.md`: codable yes/partly/no, what is lost, data needed and available, look-ahead risk.
2. Write codable rules into `work/rules.py` as `def name(df, **params) -> pd.Series` (-1/0/1), using
   `rekit.indicators`. Add a baseline rule where a hypothesis compares "with vs. without" a condition.
3. Rules marked "no" stay in the matrix with the reason. Never drop them silently.
4. Deliver with evidence; the CIO reviews with `/review`. End with the four lines from `AGENTS.md` §5.
