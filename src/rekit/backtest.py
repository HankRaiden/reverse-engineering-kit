"""Bar-based backtest engine.

Rules that keep it honest:
- A signal computed on the close of bar t is filled at the OPEN of bar t+1.
- If stop and target are both inside one bar, the stop is assumed to have hit first.
- A bar that opens beyond the stop fills at that open (gap risk), not at the stop.
- Results are in R (multiples of the initial risk) and in percent of the account. Never in money.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from .indicators import atr

TRADE_COLUMNS = ["symbol", "side", "entry_ts", "exit_ts", "entry", "exit", "stop", "r_multiple",
                 "return_pct", "exit_reason"]


@dataclass(frozen=True)
class BacktestConfig:
    risk_pct: float = 1.0       # % of account risked per trade (distance entry -> stop)
    fee_bps: float = 5.5        # per side, in basis points of notional
    slippage_bps: float = 2.0   # adverse slippage on market fills (entry and stop), per side
    stop_atr: float = 1.5       # stop distance in ATRs
    target_r: float = 2.0       # target in multiples of the stop distance
    max_bars: int | None = None  # optional time exit
    atr_n: int = 14


@dataclass
class Position:
    side: int
    entry_i: int
    entry_ts: pd.Timestamp
    entry: float
    stop: float
    target: float
    dist: float


@dataclass
class BacktestResult:
    trades: pd.DataFrame
    equity: pd.Series
    config: BacktestConfig = field(default_factory=BacktestConfig)


def _open_position(side: int, i: int, ts: pd.Timestamp, open_px: float, atr_prev: float,
                   cfg: BacktestConfig) -> Position:
    slip = cfg.slippage_bps / 1e4
    entry = open_px * (1 + side * slip)
    dist = cfg.stop_atr * atr_prev
    return Position(side, i, ts, entry, entry - side * dist, entry + side * cfg.target_r * dist, dist)


def _step_position(pos: Position, i: int, o: float, h: float, lo: float, c: float, is_last: bool,
                   cfg: BacktestConfig) -> tuple[float, str] | None:
    """Check one bar for an exit. Returns (exit_price, reason) or None. Shared by backtest and paper trading."""
    slip = cfg.slippage_bps / 1e4
    s = pos.side
    # 1) gap through the stop at the open
    if (s == 1 and o <= pos.stop) or (s == -1 and o >= pos.stop):
        return o * (1 - s * slip), "stop"
    # 2) stop inside the bar (checked before the target: conservative)
    if (s == 1 and lo <= pos.stop) or (s == -1 and h >= pos.stop):
        return pos.stop * (1 - s * slip), "stop"
    # 3) target (limit order, no slippage)
    if (s == 1 and h >= pos.target) or (s == -1 and lo <= pos.target):
        return pos.target, "target"
    if cfg.max_bars is not None and i - pos.entry_i + 1 >= cfg.max_bars:
        return c, "time"
    if is_last:
        return c, "end"
    return None


def _close(pos: Position, exit_px: float, ts: pd.Timestamp, reason: str, symbol: str,
           cfg: BacktestConfig) -> dict:
    fees_r = 2 * cfg.fee_bps / 1e4 * pos.entry / pos.dist
    r = pos.side * (exit_px - pos.entry) / pos.dist - fees_r
    return {"symbol": symbol, "side": pos.side, "entry_ts": pos.entry_ts, "exit_ts": ts, "entry": pos.entry,
            "exit": exit_px, "stop": pos.stop, "r_multiple": r, "return_pct": r * cfg.risk_pct,
            "exit_reason": reason}


def run_backtest(df: pd.DataFrame, signal: pd.Series, cfg: BacktestConfig | None = None,
                 symbol: str = "") -> BacktestResult:
    cfg = cfg or BacktestConfig()
    sig = signal.reindex(df.index).fillna(0).astype(int).to_numpy()
    a = atr(df, cfg.atr_n).to_numpy()
    o, h, lo, c = (df[k].to_numpy() for k in ("open", "high", "low", "close"))
    idx = df.index
    n = len(df)
    trades: list[dict] = []
    pos: Position | None = None
    for i in range(1, n):
        if pos is None and sig[i - 1] != 0 and np.isfinite(a[i - 1]) and a[i - 1] > 0:
            pos = _open_position(int(np.sign(sig[i - 1])), i, idx[i], o[i], a[i - 1], cfg)
        if pos is not None:
            hit = _step_position(pos, i, o[i], h[i], lo[i], c[i], i == n - 1, cfg)
            if hit:
                trades.append(_close(pos, hit[0], idx[i], hit[1], symbol, cfg))
                pos = None
    tr = pd.DataFrame(trades, columns=TRADE_COLUMNS)
    growth = pd.Series(1.0, index=idx)
    if len(tr):
        per_bar = (1 + tr.return_pct / 100).groupby(tr.exit_ts).prod()
        growth.loc[per_bar.index] = per_bar.to_numpy()
    return BacktestResult(trades=tr, equity=growth.cumprod().rename("equity"), config=cfg)
