# Methodology: why the numbers of this kit hold up

Most backtests online are not lies. They are just too kind. The kit builds five walls against the most common
ways of fooling yourself.

## 1. Pre-registration instead of bending afterwards
Before any number is computed, it is fixed what is tested, how it is measured, when it counts as refuted, and how
many trades that needs. After the CHAIRMAN-GO, `rekit lock` freezes the file by SHA-256. `rekit backtest` refuses
any changed file.
**Why:** whoever adjusts the rules after seeing the result ends up measuring how well they can adjust.

## 2. No peeking into the future (look-ahead)
- A signal is computed on the **close** of a candle and filled at the **open of the next** one.
- Swing highs and lows are only known once the confirming candles have closed. `rekit` reports them that late.
- `rekit check-lookahead` randomly changes all data **after** a time t. If that moves any signal **before** t, the
  rule looks into the future, and the check fails.
**Why:** in a real project an idea looked like +47% in a naive backtest. With real execution times it was −32.7%.

## 3. Realistic rather than optimistic execution
Fees on both sides, slippage on market fills and stops, gaps through the stop (filled at the open, not at the stop
price). If stop and target fall in the same candle, the stop counts as hit first.

## 4. Statistics that expect randomness
| Tool | Question it answers |
|------|---------------------|
| Bootstrap confidence interval (1,000×) | How sure is the expectancy if the trades had fallen differently by chance? |
| Deflated Sharpe (Bailey & López de Prado) | How likely is the result real, given I tried N variants? |
| Holm correction | Do several hypotheses hold at once, or did one just "win" by chance? |
| Power analysis (`min_trades`) | How many trades do I need to see an effect of this size at all? |
| Walk-forward | If I pick parameters on the past, do they hold in the following, unseen period? |

The verdict is mechanical:
- **HOLD:** fewer trades than registered. Neither yes nor no.
- **ACCEPT:** the lower bound of the 95% interval clears the threshold, the deflated-Sharpe probability is at
  least 0.95, and the hypothesis stays significant after Holm correction.
- **REJECT:** everything else.

## 5. Concentration: the most uncomfortable question
`concentration()` shows how much of the result comes from the best three trades or the best symbol, and what is
left without them. A result that hangs on three trades is not a rule set, it is luck with bookkeeping.
In the project this kit comes from, exactly this was the most important finding (see [Lessons from live trading](lessons-from-live.md)).

## What the methodology cannot do
It does not prove the future. ACCEPT means: "in this data, with these pre-registered rules, the effect is unlikely
to be chance." Markets change. That is why ACCEPT is followed by paper trading, not by real money.
