# Backtest report

_Verdicts follow criteria registered before the test. HOLD means: not enough trades to decide._

spec: 05-hypotheses.toml · n_trials: 4 · rekit: 0.1.0 · created: 2026-11-16

| Hypothesis | Verdict | Tested metric | 95% confidence interval (R) | Trades | Hit rate | Profit factor | Expectancy (R) | Max drawdown (%) | p (Holm-adjusted) |
|---|---|---|---|---|---|---|---|---|---|
| H1 | **REJECT** | expectancy +0.059 | [-0.010, +0.121] | 2011 | 37 % | 1.09 | +0.059 | -60.8 | 0.140 |
| H2 | **REJECT** | difference vs. baseline +0.008 | [-0.088, +0.097] | 2011 | 37 % | 1.09 | +0.059 | -60.8 | 0.864 |
| H3 | **REJECT** | expectancy -0.068 | [-0.129, -0.006] | 1924 | 33 % | 0.90 | -0.068 | -82.7 | 0.983 |
| H4 | **REJECT** | difference vs. baseline +0.031 | [-0.070, +0.126] | 1651 | 38 % | 1.14 | +0.089 | -50.6 | 0.785 |

## H1 — A breakout confirmed by volume has a positive expectancy per trade

- **Verdict:** REJECT
- **Why:** expectancy +0.059 R, 95% CI [-0.010, +0.121], deflated-Sharpe probability 0.78 over 4 tried variants
- **Total return (%):** +163.3
- **Sharpe (annual):** 0.64
- **Deflated-Sharpe probability:** 0.78
- **Concentration:** Share of net result from top 3 trades (%): 5 · Net result without top 3 trades (R): +111.9

## H2 — Requiring volume improves the breakout compared with the same breakout without volume

- **Verdict:** REJECT
- **Why:** difference +0.008 R, 95% CI [-0.088, +0.097] does not clear +0.00
- **Total return (%):** +163.3
- **Sharpe (annual):** 0.64
- **Deflated-Sharpe probability:** –
- **Concentration:** Share of net result from top 3 trades (%): 5 · Net result without top 3 trades (R): +111.9

## H3 — A swing failure (sweep of the last swing point and close back inside) has a positive expectancy

- **Verdict:** REJECT
- **Why:** expectancy -0.068 R, 95% CI [-0.129, -0.006], deflated-Sharpe probability 0.00 over 4 tried variants
- **Total return (%):** -77.6
- **Sharpe (annual):** -0.79
- **Deflated-Sharpe probability:** 0.00
- **Concentration:** Share of net result from top 3 trades (%): -5 · Net result without top 3 trades (R): -136.4

## H4 — Trading the volume breakout only with the 200-EMA trend improves it

- **Verdict:** REJECT
- **Why:** difference +0.031 R, 95% CI [-0.070, +0.126] does not clear +0.00
- **Total return (%):** +267.4
- **Sharpe (annual):** 0.85
- **Deflated-Sharpe probability:** –
- **Concentration:** Share of net result from top 3 trades (%): 4 · Net result without top 3 trades (R): +141.6
