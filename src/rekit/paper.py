"""Paper trading: the backtest's exact entry/exit logic, run forward on closed candles. No orders, ever."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from .backtest import BacktestConfig, Position, _close, _open_position, _step_position
from .indicators import atr


class PaperTrader:
    def __init__(self, rule, cfg: BacktestConfig, journal: Path, symbol: str = ""):
        self.rule, self.cfg, self.journal, self.symbol = rule, cfg, Path(journal), symbol
        self.pos: Position | None = None
        self.last_ts: pd.Timestamp | None = None

    def _log(self, event: dict) -> None:
        self.journal.parent.mkdir(parents=True, exist_ok=True)
        with self.journal.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, default=str) + "\n")

    def on_bar(self, df_closed: pd.DataFrame) -> list[dict]:
        """Process the newest CLOSED candle. Calling again for the same candle does nothing."""
        if len(df_closed) < 2 or df_closed.index[-1] == self.last_ts:
            return []
        self.last_ts = df_closed.index[-1]
        i = len(df_closed) - 1
        events: list[dict] = []
        if self.pos is None:
            sig = int(self.rule(df_closed).iloc[i - 1])
            a = atr(df_closed, self.cfg.atr_n).iloc[i - 1]
            if sig != 0 and np.isfinite(a) and a > 0:
                self.pos = _open_position(int(np.sign(sig)), i, df_closed.index[i], df_closed.open.iloc[i], a, self.cfg)
                events.append({"event": "open", "ts": self.pos.entry_ts, "side": self.pos.side,
                               "entry": self.pos.entry, "stop": self.pos.stop, "target": self.pos.target})
        if self.pos is not None:
            bar = df_closed.iloc[i]
            # bars held are counted by timestamp, so a sliding window of fixed length still reaches max_bars
            held = int((df_closed.index >= self.pos.entry_ts).sum())
            hit = _step_position(self.pos, self.pos.entry_i + held - 1, bar.open, bar.high, bar.low, bar.close,
                                 False, self.cfg)
            if hit:
                t = _close(self.pos, hit[0], df_closed.index[i], hit[1], self.symbol, self.cfg)
                events.append({"event": "close", **t})
                self.pos = None
        for e in events:
            self._log(e)
        return events
