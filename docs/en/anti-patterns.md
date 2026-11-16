# 14 anti-patterns from a real project

Each of these patterns cost time, money or trust in the original project. They are phrased generally so they
apply to any strategy and any broker.

| # | Anti-pattern | What happens | Counter-measure |
|---|--------------|--------------|-----------------|
| 1 | "No error" = "success" | An exchange reply without an error was taken as a stop being set. The position was unprotected for hours. | Check the reply explicitly, then read the state back from the exchange. |
| 2 | Local state instead of exchange state | The program believed a stop was active; the exchange knew nothing of it. | The exchange is the truth. Independent reconciliation at fixed intervals. |
| 3 | Changing state before the action succeeds | The new value was already in memory; the "old = new" check skipped the call. | Change state only after confirmed success. |
| 4 | Calculating profit yourself | Local calculation and exchange settlement drifted apart and led to wrong decisions for 48 hours. | Always take the result from the exchange's settlement. |
| 5 | New close path without booking | A new way to close positions forgot to book capital. The bookkeeping drifted for weeks. | Keep a list of all close paths. Every new path goes there first. |
| 6 | Look-ahead in the backtest | +47% on paper, −32.7% with real times. | Fill on the next candle, `rekit check-lookahead`. |
| 7 | Daily data for intraday decisions | A "regime signal" used the daily close, which was not known yet at decision time. | Point-in-time data, check timestamps. |
| 8 | Result hangs on a few trades | Almost all profit came from a few small coins with price spikes. | `concentration()` in every report. |
| 9 | Too optimistic execution model | The backtest filled limit orders that would never have filled in reality. | Conservative fill rules. Paper trading compares with reality. |
| 10 | More symbols = more diversification | 588 symbols, but effectively only about 1.7 independent bets: crypto moves as one factor. | Measure correlation instead of counting symbols. |
| 11 | Trading more = earning more | Every higher frequency worsened all risk metrics. | Test frequency as a hypothesis, do not assume it. |
| 12 | Shipping configuration without code | A config switch pointed to code that was not on the server yet. The feature stayed silently off. | Always ship config and code together, then verify. |
| 13 | Evidence nobody re-checked | An agent reported test results that never ran. | Every number with command and output. Invented evidence leads to REJECT automatically. |
| 14 | Rediscovering what was refuted | The same attractive idea came up "new" every few weeks. | Refutation register with a condition for reopening. |
