# Lessons from live trading

This kit comes from a real project. A crypto bot, built from publicly available trading knowledge, was run by two
AI agents and controlled by one human. It traded from **18 February to 29 July 2026** on Bybit with deliberately
small **own capital**.

> **The bot itself is not part of this kit and will not be published.** Here are the lessons only, in percent only,
> without parameters. None of these numbers is a forecast or a recommendation.

## What was measured
| Finding | Number | Window |
|---------|--------|--------|
| Time-weighted return (measures the strategy) | +35.0% | 20 Feb – 29 Jul 2026 |
| … of which from the rule set of 1 April on | +31.1% | 1 Apr – 29 Jul 2026 |
| Bitcoin in the same window | −4.8% and −6.2% | the same windows |
| Money-weighted return (measures the account, modified Dietz) | +14.7% | 18 Feb – 29 Jul 2026 |
| Net result in % of all money ever paid in | +5.0% | 18 Feb – 29 Jul 2026 |
| Largest drawdown (time-weighted) | −21.4% | 20 Feb – 29 Jul 2026 |
| Learning phase: profit factor of the first ~170 trades | 1.00 (exactly break-even) | Feb–Mar 2026 |

**Sensitivity:** on 30 March the internally booked capital was aligned with the exchange wallet for the first time. If
three small deposits are booked there instead, the result is +34.4% instead of +35.0% and a largest drawdown of −18.4%
instead of −21.4%. All returns were recalculated by a second auditor with independent code.

**Why two such different returns?** The profit was made mostly in April on a small capital base. More capital came
in afterwards, and the strategy ran at roughly zero. Time-weighted measures the strategy, money-weighted measures the
account. Both are true. Showing only one hides the other.

## The most important lesson: concentration
| Period | Total | Without small coins with price spikes |
|--------|-------|----------------------------------------|
| April–May | +35.7% | +3.7% (small coins brought 95% of the profit) |
| June–July | −3.0% | −0.8%; also without TON, a single large winner, −8.5% |

Method: result in the window relative to the capital at the start of the window, an approximation without path
effects.

The return came almost entirely from a few episodes of small coins with strong price spikes. On large, liquid
coins the same logic ran flat to negative. That is why every report of this kit includes `concentration()`.

## What was refuted
| Idea | Result |
|------|--------|
| Longer holding brings +47% | Refuted: with real times it was −32.7% (look-ahead). |
| Double leverage doubles the profit | Refuted: risk limits bind first, and one liquidation came on top. |
| Tighter trailing protects profits | Refuted: every alternative was worse. |
| Cancelled limit orders filter out losers | Refuted: the confidence interval includes zero. |
| Avoid illiquid coins | Refuted: the most illiquid coins were the biggest winners (see concentration). |
| More coins bring more diversification | Refuted: effectively about 1.7 independent bets remained. |
| Market breadth as a regime light | Refuted: the effect was a look-ahead artefact. |
| Trading more brings more | Refuted: every higher frequency worsened all risk metrics. |
| Finding better entry filters | Refuted: over 7,874 out-of-sample signals, no filter measurably improved the result. |

**Pattern:** what survived the tests almost always took something away, such as losing time windows, meme coins or
unmapped symbols. Adding things practically never helped.

## The pause
On 29 July the bot was paused. A simulation with the unchanged code over the following 56 days gave a median of
+2.4% (middle 90% of paths: −4.9% to +19.3%). Bitcoin rose +34.1% in the same period. The bot would have captured
only a small part of that rise.
