# Stage 8 · Paper-trading plan

> Who: CIO + CTO · Output: `work/08-paper-plan.md` · **Gate: CHAIRMAN-GO to start**
> Paper trading means: real prices, fictitious trades, no money, no orders.

## What is tested
- Hypothesis: H<N> (backtest verdict: ACCEPT · REJECT · HOLD)
- If the verdict is not ACCEPT: **why paper trade anyway?** (e.g. for learning only, clearly labelled)

## Procedure
- Command: `rekit paper work/05-hypotheses.toml --hypothesis H<N> --symbol <SYMBOL>`
- Journal: `work/paper-H<N>-<symbol>.jsonl`
- Duration: at least N trades or M weeks, whichever comes later

## Stop and success criteria, fixed in advance
| Criterion | Limit | Action |
|-----------|-------|--------|
| Expectancy after N trades | below the backtest CI | stop, back to stage 5 |
| Max drawdown | e.g. −15% | pause, root-cause analysis |
| Paper vs. backtest deviation per trade | > X R | check the execution model |

## Weekly rhythm
Weekly review with `templates/en/weekly-review.md`; every close with `templates/en/post-mortem.md`.

## Chairman
`CHAIRMAN-GO: paper start H<N> is approved.`
