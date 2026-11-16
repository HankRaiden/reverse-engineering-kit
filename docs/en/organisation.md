# The organisation: two agents, one challenger, one human

The most important idea of the kit is not a formula but a **separation of powers**. No agent may decide on its own
what counts as proven.

## Roles
| Role | Who | May | May not |
|------|-----|-----|---------|
| **Chairman** | you | give GO / HOLD / NO-GO at the gates, veto any decision | be talked into technicalities without seeing the evidence |
| **CIO** | AI agent | profile the source, formulate principles and rules, write assignments, review deliveries (0–100) | calculate or write code, skip gates |
| **CTO** | AI agent | code the rules, run `rekit`, deliver with evidence | write own statistics, change locked files, send orders |
| **Challenger** | AI agent | attack every result (6 mandatory questions), write refutations to the register | sugar-coat |

## Two classes of work
- **ANALYSIS:** reading, summarising, backtests, reports. The agents work on their own.
- **DECISION:** selecting principles, pre-registration, paper start. This work starts only with the literal
  sentence `CHAIRMAN-GO: …`. Every decision is written to `work/approval-log.jsonl`.

## The loop
```
CIO writes assignment ──► [gate, if DECISION: chairman GO / HOLD / NO-GO]
        ▲                                │ GO
        │ HOLD / NO-GO: back             ▼
CIO reviews ◄── challenger attacks ◄── CTO builds, tests, delivers with evidence
```

## Four items in every agent answer
1. **Verdict:** ACCEPT · ACCEPT_WITH_CONDITIONS · HOLD · REJECT
2. **Class:** ANALYSIS or DECISION
3. **Next gate:** what must be true before the next step
4. **Whose turn:** CIO, CTO or chairman

So in every message you see within five seconds whether you are needed.

## Why so much form?
Because AI agents phrase things very convincingly, even when they are wrong. In the project this kit comes from,
more than 150 formal assignments and more than 100 reviews went through exactly this loop. The most expensive
mistakes happened where it was bypassed.

## Example
A complete assignment with its review lives in `examples/beispiel-emperorbtc-oeffentlich/work/`.
