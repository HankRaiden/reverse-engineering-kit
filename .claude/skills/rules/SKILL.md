---
name: rules
description: Stage 3 — turn the approved principles into unambiguous if-then rules (the MD export). Use after gate 1.
---
Role: **CIO**. Class: ANALYSIS.

1. Check `work/approval-log.jsonl` for gate 1. Without it: stop and say so.
2. For each approved principle write rule(s) with `templates/<lang>/rules-spec.md` into `work/03-rules.md`:
   market, timeframe, long/short entry, stop, target, risk per trade, parameters with their origin, execution timing.
3. Mark every number the source does not give as **own assumption**. Count them; they become extra trials.
4. Next step: `/codability` (write a CTO assignment with `/assignment`). End with the four lines from `AGENTS.md` §5.
