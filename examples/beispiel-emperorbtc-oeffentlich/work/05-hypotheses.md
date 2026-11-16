# Stage 5 · Pre-registration

> Machine part: `05-hypotheses.toml` · Locked after CHAIRMAN-GO: `05-hypotheses.toml.lock`

| ID | Statement | Metric | Rejected if | Min. trades |
|----|-----------|--------|-------------|-------------|
| H1 | Volume breakout has a positive expectancy | `expectancy_r` | lower 95% CI bound ≤ 0 R, or deflated-Sharpe probability < 0.95, or Holm-adjusted p > 0.05 | 270 |
| H2 | Volume makes the breakout better than without | `expectancy_diff_r` vs. R1b | lower 95% CI bound of the difference ≤ 0 | 270 |
| H3 | Swing failure has a positive expectancy | `expectancy_r` | as H1 | 270 |
| H4 | The 200-EMA filter improves the volume breakout | `expectancy_diff_r` vs. R1 | lower 95% CI bound of the difference ≤ 0 | 270 |

- **Minimum sample:** `rekit.stats.min_trades(0.2, 1.3)` = 262 → 270 (detect +0.2 R with sd 1.3 R).
- **Trials:** 4 hypotheses, no parameter grid → n_trials = 4. The 8 assumptions from stage 3 were fixed once and not
  tuned; had we tuned them, every combination would count.
- **Data:** Bybit public 4h candles, 5 symbols, 2022-01-01 to 2026-11-01.
- **Look-ahead check:** `uv run rekit check-lookahead 05-hypotheses.toml` → green for all four rules.
