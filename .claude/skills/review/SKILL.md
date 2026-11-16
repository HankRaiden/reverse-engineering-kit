---
name: review
description: The CIO reviews a CTO or challenger delivery: re-runs evidence, checks every F-check and NAK, scores 0–100 and gives a verdict. Use after every delivery.
---
Role: **CIO**. Class: ANALYSIS.

1. Use `templates/<lang>/review.md`; save as `work/reviews/<date>-<title>.md`.
2. Re-run at least one command from the delivery yourself (e.g. `uv run rekit check-lookahead …`) and compare.
3. Any invented or unverifiable evidence → REJECT, regardless of the rest.
4. Name the next gate and whose turn it is. End with the four lines from `AGENTS.md` §5.
