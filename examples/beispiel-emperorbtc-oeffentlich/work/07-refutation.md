# Stage 7 · Refutation register

> Challenger on `06-backtest/en/results.json` · verdict by CIO

| ID | Hypothesis | Test | Result | Verdict | Why it sounded plausible | Reopen only if … |
|----|-----------|------|--------|---------|--------------------------|-------------------|
| W1 | H1 volume breakout > 0 R | 5 perps, 4h, 2022-01 – 2026-10, 2,011 trades | +0.059 R, CI [−0.010, +0.121], DSR 0.78, p_Holm 0.140 | REJECT | +163% total return looks like an edge | a new, pre-registered test on other data (e.g. other coins or 2018–2021) clears the CI |
| W2 | H2 volume makes breakouts better | same, vs. breakout without volume | difference +0.008 R, CI [−0.088, +0.097] | REJECT | the core of the volume teaching | a different, pre-registered volume definition (e.g. relative to the session) |
| W3 | H3 swing failure > 0 R | 1,924 trades | −0.068 R, CI [−0.129, −0.006] | REJECT (negative) | stop hunts are visible on every chart | context filters from the original (higher timeframe, volume on the sweep) are coded and pre-registered |
| W4 | H4 200-EMA filter improves R1 | 1,651 vs. 2,011 trades | difference +0.031 R, CI [−0.070, +0.126] | REJECT | "trade with the trend" is the most common advice | — |

## The six mandatory questions
1. **Look-ahead:** re-ran `rekit check-lookahead`: green. Range excludes the current candle; swing points only after
   3 confirming candles.
2. **Variants:** 4 hypotheses counted. The 8 assumptions from stage 3 were not tuned. Had we tried several lookbacks
   or multiples, the bar would be higher still.
3. **Concentration:** top 3 trades carry only 5% (H1) / 4% (H4) of net R, so the results are not driven by single
   trades. By symbol, the best symbol carries 59% (H1) / 34% (H4) of net R.
4. **Out of sample:** no grid, so these are full-period results with fixed parameters. No in-sample tuning took place,
   but there is also no walk-forward confirmation.
5. **Costs:** 5.5 bps fee + 2 bps slippage per side are realistic for liquid perps; small coins would cost more.
6. **Another period:** 2022 was a bear market, 2023–2024 a bull market. A test on 2018–2021 would be a new
   hypothesis with its own registration.

## What this does and does not say
It refutes **our coded versions** of three principles on five large coins. It says nothing about how EmperorBTC
trades them with context and judgement, and nothing about P5–P7 (not tested). That is exactly the gap between a
discretionary trader and a rule.
