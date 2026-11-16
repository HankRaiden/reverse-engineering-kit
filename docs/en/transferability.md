# What transfers and what does not

## What transfers
The kit is not tied to crypto. It works with any public playbook, any strategy and any principle of your own, as
long as three things hold:
1. **The rules can be phrased as if-then**, even only partly (stage 4 names the rest).
2. **Historical price data exists** at the right resolution (candles with open, high, low, close, volume).
3. **The broker or exchange offers a stable API**, at the latest when you move on by yourself after paper trading.

## How to recognise a stable API
| Criterion | Why it matters |
|-----------|----------------|
| Versioned, documented endpoints | So nothing changes silently |
| Explicit error codes in every reply | "No error" is not "success" (anti-pattern 1) |
| Stop loss can be set and read directly on the exchange | Protection that works even without your program |
| Settlement per trade can be fetched | The result comes from the exchange, not from your own calculation |
| Test or demo environment | Paper trading and execution tests without money |
| Public market data without an account | Backtests without keys |

## Other markets
- **Stocks and ETFs:** mind dividends, splits, trading hours and overnight gaps. Gaps through the stop are more
  common there.
- **Futures:** mind contract rolls and margin rules.
- **FX:** spreads change a lot by session. Calculate slippage conservatively.

Plug in your own data via CSV (`ts, open, high, low, close, volume`) and use `--csv-dir`.

## What does not transfer
- The gut feeling of a discretionary trader. What is not described cannot be coded.
- Results from one market to another. Every transfer is a new hypothesis.
