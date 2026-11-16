# Stage 4 · Codability matrix

> Who: CTO · Code: `rules.py`

| Principle / rule | Codable? | What is lost when coding it? | Data | Available? | Look-ahead risk | Decision |
|------------------|----------|------------------------------|------|------------|-----------------|----------|
| P1 → R1 volume breakout | yes | the trader's judgement of *which* range matters | OHLCV | yes | range must exclude the current candle | **test (H1, H2)** |
| P2 → R2 swing failure | yes | higher-timeframe context, volume on the sweep | OHLCV | yes | swing points only after confirmation (`rekit.indicators.swing_high`) | **test (H3)** |
| P3 → R3 200 EMA trend | yes | – | OHLCV | yes | none (causal EMA) | **test (H4)** |
| P4 fixed risk | yes | – | – | – | – | built into every backtest |
| P5 open interest | partly | interpretation of OI vs. price | OI history | public OI history is short on many exchanges | daily OI snapshots can leak the close | **not tested** in this example |
| P6 divergence | partly | which pivots count | OHLCV | yes | pivot confirmation | **not tested** here (keeps the number of trials low) |
| P7 survival | no (as a signal) | – | – | – | – | process rule in stage 8 |

Honesty note: three of seven principles are not tested. A result below says nothing about them.
