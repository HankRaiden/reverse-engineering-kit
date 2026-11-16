---
name: preregister
description: Stage 5 — write the hypotheses with metrics, rejection criteria and minimum sample, get CHAIRMAN-GO (gate 2), then lock the file. Use after /codability.
---
Role: **CIO**, lock by **CTO**. Class: DECISION (gate 2).

1. Write `work/05-hypotheses.md` with `templates/<lang>/preregistration.md` and the machine part
   `work/05-hypotheses.toml` with `templates/<lang>/hypotheses.toml`.
2. Justify `min_trades` with `rekit.stats.min_trades(effect_r, sd_r)` (ask the CTO to run it). Use a grid only if
   needed; every combination is a trial and is judged out of sample.
3. The CTO runs `uv run rekit check-lookahead work/05-hypotheses.toml`. It must be green.
4. Present the hypotheses and the total number of trials to the chairman. Ask for:
   `CHAIRMAN-GO: pre-registration work/05-hypotheses.toml is approved.`
5. Only after that sentence: `uv run rekit lock work/05-hypotheses.toml` and record the decision with `/chairman`
   (include the sha256 from the `.lock` file).
6. End with the four lines from `AGENTS.md` §5.
