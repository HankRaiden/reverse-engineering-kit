---
name: chairman
description: Shows the chairman which gate is open and whose turn it is, asks for GO / HOLD / NO-GO and appends the decision to the approval log. Use whenever a decision is needed or the chairman asks for status.
---
For the **chairman**. Keep it short.

1. Read `work/` and `work/approval-log.jsonl`. Show: current stage, open gate (1 principles, 2 pre-registration,
   3 paper start), whose turn it is, and the one decision needed now, with its options.
2. Ask the chairman with a question tool (options GO / HOLD / NO-GO). A gate passes only on the literal sentence
   `CHAIRMAN-GO: …` or the explicit GO option; silence is never approval.
3. Append one JSON line to `work/approval-log.jsonl` following `templates/<lang>/approval-log.schema.json`
   (ts in UTC, gate, decision, the chairman's exact words, files, sha256 if a `.lock` exists).
4. On HOLD or NO-GO: say what goes back to whom. End with the four lines from `AGENTS.md` §5.
