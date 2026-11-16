# Stage 8 · Paper-trading plan

> Who: CIO + CTO · Gate 3

## Decision
**No paper start recommended.** None of the four hypotheses is ACCEPT. Paper trading a REJECT would only produce noise
that feels like learning.

## If the chairman still wants to learn the workflow
Only labelled as an exercise, with the least bad candidate H1:
- Command: `uv run rekit paper work/05-hypotheses.toml --hypothesis H1 --symbol BTC/USDT:USDT`
- Journal: `work/paper-H1-BTC-USDT-USDT.jsonl`
- Duration: 60 trades or 12 weeks, whichever comes later.

| Criterion | Limit | Action |
|-----------|-------|--------|
| Expectancy after 60 trades | below −0.043 R (lower CI bound of H1) | stop |
| Max drawdown | −15% | stop, post-mortem |
| Paper vs. backtest per trade | > 0.1 R | check the execution model |

## Better next step
Back to stage 3: code the context the original teaching relies on (higher timeframe, volume on the sweep) as new,
pre-registered hypotheses — and count them as new trials.

Gate 3 is therefore not requested. See `docs/en/after-paper-trading.md` and `DISCLAIMER.md`.
