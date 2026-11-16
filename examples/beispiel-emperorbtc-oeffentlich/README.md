# Worked example: EmperorBTC's public principles, reverse-engineered

[Deutsch](README.de.md) · [Disclaimer](../../DISCLAIMER.md)

> Independent example, **not affiliated with EmperorBTC**. Principles are summarised in our own words with links to
> his public threads. **I accept no responsibility for any results that may be obtained in connection with this
> project.** Not financial advice.

All eight stages, done once, so you can see what each produces. Files live in [`work/`](work/).

| Stage | File | What came out |
|-------|------|---------------|
| 1 Source | [01-source.md](work/01-source.md) | public X threads, Telegram index, tutorial sheet |
| 2 Principles | [02-principles/](work/02-principles/) | 7 cards: volume, swing failure, 200 EMA, fixed risk, open interest, divergence, survival |
| 3 Rules | [03-rules.md](work/03-rules.md) | 3 rules + 1 baseline, 8 own assumptions marked |
| 4 Codability | [04-codability.md](work/04-codability.md) | 3 of 7 principles not tested, with reasons |
| 5 Pre-registration | [05-hypotheses.md](work/05-hypotheses.md) | 4 hypotheses, min. 270 trades each, locked |
| 6 Backtest | [06-backtest/en/report.md](work/06-backtest/en/report.md) | 5 perps, 4h, 2022-01 – 2026-10 |
| 7 Refutation | [07-refutation.md](work/07-refutation.md) | six mandatory questions answered |
| 8 Paper plan | [08-paper-plan.md](work/08-paper-plan.md) | no paper start recommended |

## The result, honestly
| Hypothesis | Verdict | Key number |
|-----------|---------|------------|
| H1 Breakout with volume > 0 R | **REJECT** | +0.059 R per trade, 95% CI [−0.010, +0.121] — despite +163% total return |
| H2 Volume improves breakouts | **REJECT** | difference +0.008 R, CI [−0.088, +0.097] |
| H3 Swing failure > 0 R | **REJECT** | −0.068 R, CI [−0.129, −0.006]: negative |
| H4 200-EMA filter improves H1 | **REJECT** | difference +0.031 R, CI [−0.070, +0.126] |

**What this means:** our coded versions of these principles did not show a robust edge on five large coins. It does
**not** mean the trader is wrong: the discretionary context he teaches is exactly what the rules leave out
(stage 4). That gap is the real insight, and it matches what the live project behind this kit found: the
measurable return came from a few episodes in small coins, not from the large ones.

Reproduce: `./fetch.sh` (public data only).
