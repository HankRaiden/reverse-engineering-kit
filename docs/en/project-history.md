# Project history: from the first line to the pause, radically honest

This kit is the by-product of a real project. Here is how it went, with everything that worked and everything that
went wrong. All results refer only to **own-capital trades on Bybit** and are given in percent only. The bot itself
is not published ([why](../../SAFETY.md)).

## Timeline
| Date (2026) | Event | What it meant |
|-------------|-------|---------------|
| 11 Feb | Day zero: trading engine, walk-forward tester, first tests | Built in AI-agent sessions, not by hand |
| 18–19 Feb | Live with deliberately small own capital, first closed trade | No demo phase first. A mistake the kit now avoids with paper trading. |
| Feb–Mar | Learning phase: about 170 trades, profit factor **1.00** | The bot earned nothing but survived. Every mistake became a rule. |
| Feb–Apr | **14 documented incidents**, among them a position 5 hours without a stop loss, stops silently dropped by a third-party library (undetected for 15 days), bookkeeping 12.3% off the exchange | These produced the 7 architecture principles and the [14 anti-patterns](anti-patterns.md) |
| 16 Mar | Pre-defined criterion met: 30 of 30 trades with stable stop loss | First formal gate passed |
| Mar–Apr | 32 data-driven changes, each justified and tested | Most of those that survived *took something away* (time windows, meme coins) |
| April | Strongest month: **+33.9%** time-weighted | Almost entirely from a few small coins with price spikes. Named as a risk early on. |
| May | Capital increased. Afterwards the strategy runs at roughly **zero**. | Money-weighted and time-weighted returns diverge widely from here on |
| May–Jul | In parallel, a **fully autonomous attempt** on a second own-capital account: the agents could put strategies live without chairman approval. | Practically dormant from 5 June, zero new robust edges, running costs above the return. Shut down. The human at the gates was not bureaucracy, it was the part that worked. |
| 16 Jun | Independent recalculation: **+34.6%** time-weighted since 1 April vs. Bitcoin **−3.3%** | Real performance in that window, but short and concentrated |
| Jun–Jul | "Quantum-leap investigation": five analyses refuted seven apparent improvements | No further lever in the rule set |
| 8 Jul | Chairman deliberately reduces capital (de-risk) | A human decision, not the agents' |
| 29 Jul | Chairman pauses the bot, no open position | End of the own-capital live phase. Balance: **+35.0%** time-weighted (Bitcoin −4.8%), +14.7% money-weighted, −14.7% below the high |
| 28 Aug | Server shut down, complete archive secured | |
| 23 Sep | Simulation "what would the bot have earned without the pause?" over 56 days: median **+2.4%**, Bitcoin **+34.1%** | The pause cost little. Against simply holding Bitcoin the bot would have lost clearly. |
| Nov | This kit: the method is shared, the bot is not | |

## Balance
| Successes | Failures |
|-----------|----------|
| A live track record with real money instead of backtest poetry | Learning phase practically break-even (profit factor 1.00) |
| +35.0% time-weighted over the live phase vs. Bitcoin −4.8%, interim result recalculated independently | The profit hung on a few small coins and one single coin. Without them: April–May +3.7%, June–July −8.5% |
| A forensic check over 62 days found none of 228 positions ever opened without a stop loss | Before that, several incidents with unprotected positions |
| Nine tempting ideas cleanly refuted before they cost money | One idea looked like +47% in a naive backtest and was −32.7% in reality |
| The separation of powers CIO / CTO / chairman caught many mistakes | The fully autonomous attempt without a human at the gates failed |
| Over 150 formal assignments and over 100 reviews, every approval logged | An agent once reported test results that never ran. Since then, invented evidence leads to REJECT automatically. |
| | Money-weighted +14.7%. Measured against all money ever paid in, only +5.0% net remained. Largest drawdown −21.4%. |

| Opportunities | Risks |
|---------------|-------|
| Public knowledge can be taken apart and tested systematically, with any broker that has a stable API | A discretionary trader can never be fully coded |
| AI agents make research fast and cheap | AI agents phrase things convincingly even when wrong. Without gates and evidence that is dangerous. |
| Pre-registration and the refutation register save expensive repetitions | Short track records (months) say little about years |
| The method transfers to other markets | Leverage and small coins can cost more in hours than they bring in months |

## What we would do differently today
1. Paper trading first, live only afterwards. That is exactly why the kit ends there.
2. Put the concentration check into every report from day one.
3. Never optimise away the human at the gates.
