# Stage 3 · Rule specification (MD export)

> Who: CIO · Execution for all rules: signal on candle close, entry at the open of the next 4h candle.
> Risk per trade 1% of the account (P4). Stop 1.5 × ATR(14), target 2 R, fees 5.5 bps per side, slippage 2 bps.
> **Own assumptions** (not given by the source) are marked ⚑. There are 8 of them.

## R1 · Volume breakout (P1)
| Field | Content |
|-------|---------|
| Symbols | BTC, ETH, SOL, XRP, DOGE perpetuals (USDT), Bybit |
| Timeframe | 4h |
| Long | close > highest high of the previous 20 candles ⚑ AND volume > 1.5 ⚑ × average volume of the previous 20 candles |
| Short | close < lowest low of the previous 20 candles AND the same volume condition |
| Stop / target | 1.5 × ATR ⚑ / 2 R ⚑ |
| Baseline R1b | the same breakout without the volume condition |

## R2 · Swing failure (P2)
| Field | Content |
|-------|---------|
| Swing point | a high (low) with 3 lower highs (higher lows) on each side ⚑; known only after the 3 right candles closed |
| Short | candle high > last confirmed swing high AND close < it |
| Long | candle low < last confirmed swing low AND close > it |
| Stop / target | 1.5 × ATR / 2 R |

## R3 · Volume breakout with the trend (P1 + P3)
R1, but longs only when close > 200 EMA, shorts only when close < 200 EMA ⚑ (EMA length from the source; using it
as a hard filter is our choice).

## Assumptions ⚑
lookback 20 · volume multiple 1.5 · ATR multiple 1.5 · target 2 R · swing width 3/3 · hard EMA filter ·
universe of 5 large coins · period 2022-01 to 2026-10.
