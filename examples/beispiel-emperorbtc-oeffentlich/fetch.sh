#!/usr/bin/env bash
# Re-create the example from scratch (public data only, no account, no key).
set -euo pipefail
cd "$(dirname "$0")"
uv run rekit check-lookahead work/05-hypotheses.toml          # downloads public 4h candles into work/.cache
uv run rekit backtest work/05-hypotheses.toml --out work/06-backtest/en --lang en
uv run rekit backtest work/05-hypotheses.toml --out work/06-backtest/de --lang de
