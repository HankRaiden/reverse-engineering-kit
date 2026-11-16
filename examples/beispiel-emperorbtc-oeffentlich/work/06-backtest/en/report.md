# Backtest report

_Verdicts follow criteria registered before the test. HOLD means: not enough trades to decide._

spec: 05-hypotheses.toml · n_trials: 4 · rekit: 0.1.0 · created: 2026-11-16

| Hypothesis | Verdict | Tested metric | 95% confidence interval (R) | Trades | Hit rate | Profit factor | Expectancy (R) | Max drawdown (%) | p (Holm-adjusted) |
|---|---|---|---|---|---|---|---|---|---|
| H1 | **REJECT** | expectancy +0.059 | [-0.043, +0.156] | 2011 | 37 % | 1.09 | +0.059 | -60.8 | 0.512 |
| H2 | **REJECT** | difference vs. baseline +0.008 | [-0.131, +0.139] | 2011 | 37 % | 1.09 | +0.059 | -60.8 | 1.000 |
| H3 | **REJECT** | expectancy -0.068 | [-0.140, +0.001] | 1924 | 33 % | 0.90 | -0.068 | -82.7 | 1.000 |
| H4 | **REJECT** | difference vs. baseline +0.031 | [-0.122, +0.182] | 1651 | 38 % | 1.14 | +0.089 | -50.6 | 1.000 |

## H1 — A breakout confirmed by volume has a positive expectancy per trade

- **Verdict:** REJECT
- **Why:** expectancy +0.059 R, 95% CI [-0.043, +0.156] (not shown), deflated-Sharpe probability 0.54 over 4 tried variants
- **Total return (%):** +163.3
- **Sharpe (annual):** 0.64
- **Deflated-Sharpe probability:** 0.54
- **Concentration:** Share of net result from top 3 trades (%): 5 · Net result without top 3 trades (R): +111.9

> Total return and drawdown are exit-marked: every trade risks 1.0 % of the account at entry and is booked when it closes, across all symbols. Up to 5 positions were open at the same time (up to 5.0 % of the account at risk). This is not a specified portfolio.

> Confidence intervals resample whole calendar weeks, so trades that happened together are not counted as independent evidence.

## H2 — Requiring volume improves the breakout compared with the same breakout without volume

- **Verdict:** REJECT
- **Why:** difference +0.008 R, 95% CI [-0.131, +0.139] does not clear +0.00
- **Total return (%):** +163.3
- **Sharpe (annual):** 0.64
- **Deflated-Sharpe probability:** –
- **Concentration:** Share of net result from top 3 trades (%): 5 · Net result without top 3 trades (R): +111.9

> Total return and drawdown are exit-marked: every trade risks 1.0 % of the account at entry and is booked when it closes, across all symbols. Up to 5 positions were open at the same time (up to 5.0 % of the account at risk). This is not a specified portfolio.

> Confidence intervals resample whole calendar weeks, so trades that happened together are not counted as independent evidence.

## H3 — A swing failure (sweep of the last swing point and close back inside) has a positive expectancy

- **Verdict:** REJECT
- **Why:** expectancy -0.068 R, 95% CI [-0.140, +0.001] (not shown), deflated-Sharpe probability 0.00 over 4 tried variants
- **Total return (%):** -77.6
- **Sharpe (annual):** -0.79
- **Deflated-Sharpe probability:** 0.00
- **Concentration:** Share of net result from top 3 trades (%): -5 · Net result without top 3 trades (R): -136.4

> Total return and drawdown are exit-marked: every trade risks 1.0 % of the account at entry and is booked when it closes, across all symbols. Up to 5 positions were open at the same time (up to 5.0 % of the account at risk). This is not a specified portfolio.

> Confidence intervals resample whole calendar weeks, so trades that happened together are not counted as independent evidence.

## H4 — Trading the volume breakout only with the 200-EMA trend improves it

- **Verdict:** REJECT
- **Why:** difference +0.031 R, 95% CI [-0.122, +0.182] does not clear +0.00
- **Total return (%):** +267.4
- **Sharpe (annual):** 0.85
- **Deflated-Sharpe probability:** –
- **Concentration:** Share of net result from top 3 trades (%): 4 · Net result without top 3 trades (R): +141.6

> Total return and drawdown are exit-marked: every trade risks 1.0 % of the account at entry and is booked when it closes, across all symbols. Up to 5 positions were open at the same time (up to 5.0 % of the account at risk). This is not a specified portfolio.

> Confidence intervals resample whole calendar weeks, so trades that happened together are not counted as independent evidence.
