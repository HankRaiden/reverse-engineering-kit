# Stage 5 · Hypothesis pre-registration

> Who: CIO · Output: `work/05-hypotheses.md` + `work/05-hypotheses.toml` · **Gate: CHAIRMAN-GO, then `rekit lock`**

Once locked, the file is frozen. Anyone who changes it afterwards gets a refusal from `rekit backtest`.
New ideas go into a NEW file, and they count as additional trials.

## H<N> · <statement in one sentence>
- **Rule(s):** R<N> from `work/03-rules.md`
- **Expectation:** e.g. "expectancy > 0 R per trade"
- **Metric:** `expectancy_r` or `expectancy_diff_r` (against a baseline rule)
- **Rejection criterion:** the lower bound of the 95% confidence interval does not clear the threshold.
- **Minimum sample:** N trades (justified with `rekit.stats.min_trades`)
- **Data:** exchange, symbols, timeframe, period
- **Parameter grid (if any):** every combination counts as its own trial. Judged only out of sample (walk-forward).

## Number of trials
Sum of all variants in this file: __ (feeds the deflated-Sharpe correction)

## Chairman
`CHAIRMAN-GO: pre-registration <file> is approved.` → then `rekit lock work/05-hypotheses.toml`
