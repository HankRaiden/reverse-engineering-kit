"""OHLCV loading. Read-only: public market data from CSV or public exchange endpoints."""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

COLUMNS = ["open", "high", "low", "close", "volume"]


class DataError(ValueError):
    """Raised when market data is not fit for a backtest."""


def validate(df: pd.DataFrame, allow_gaps: bool = False) -> pd.DataFrame:
    """Sort, type-check and sanity-check an OHLCV frame. Fails loudly instead of computing on bad data."""
    missing = [c for c in COLUMNS if c not in df.columns]
    if missing:
        raise DataError(f"missing columns: {missing}")
    df = df[COLUMNS].astype(float).sort_index()
    if df.index.has_duplicates:
        raise DataError(f"duplicate timestamps, e.g. {df.index[df.index.duplicated()][0]}")
    if df.isna().any().any():
        first = df.index[df.isna().any(axis=1)][0]
        raise DataError(f"NaN values in data, first at {first}")
    if ((df.high < df[["open", "close"]].max(axis=1)) | (df.low > df[["open", "close"]].min(axis=1))).any():
        raise DataError("inconsistent OHLC: high/low do not contain open/close")
    if len(df) > 2 and not allow_gaps:
        step = df.index.to_series().diff().mode().iloc[0]
        gaps = df.index.to_series().diff() > step
        if gaps.any():
            at = df.index[gaps.to_numpy()][0]
            raise DataError(f"gap in data: candle(s) missing before {at} (expected step {step}); "
                            "pass allow_gaps=True only if you understand the consequence")
    return df


def load_csv(path: str | Path, allow_gaps: bool = False) -> pd.DataFrame:
    """Load an OHLCV CSV with a `ts` column (ISO time or epoch milliseconds)."""
    raw = pd.read_csv(path)
    if "ts" not in raw.columns:
        raise DataError("CSV needs a 'ts' column")
    ts = raw["ts"]
    if pd.api.types.is_numeric_dtype(ts):
        idx = pd.to_datetime(ts, unit="ms", utc=True)
    else:
        idx = pd.to_datetime(ts, utc=True)
    df = raw.drop(columns=["ts"]).set_index(pd.DatetimeIndex(idx, name="ts"))
    return validate(df, allow_gaps=allow_gaps)


def _cache_name(exchange: str, symbol: str, timeframe: str, start: str, end: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9]+", "-", symbol).strip("-")
    return f"{exchange}_{safe}_{timeframe}_{start}_{end}.csv"


def fetch_public_ohlcv(exchange: str, symbol: str, timeframe: str, start: str, end: str,
                       cache_dir: Path) -> pd.DataFrame:
    """Download candles from a public endpoint (no account, no key) and cache them as CSV.

    Only closed candles inside [start, end) are kept.
    """
    cache_dir = Path(cache_dir)
    cache = cache_dir / _cache_name(exchange, symbol, timeframe, start, end)
    if cache.exists():
        return load_csv(cache)
    import ccxt  # optional dependency: `uv sync --extra data`

    client = getattr(ccxt, exchange)({"enableRateLimit": True})
    since = int(pd.Timestamp(start, tz="UTC").timestamp() * 1000)
    until = int(pd.Timestamp(end, tz="UTC").timestamp() * 1000)
    rows: list[list[float]] = []
    while since < until:
        batch = client.fetch_ohlcv(symbol, timeframe, since=since, limit=1000)
        if not batch:
            break
        rows.extend(r for r in batch if r[0] < until)
        nxt = batch[-1][0] + 1
        if nxt <= since:
            break
        since = nxt
    if not rows:
        raise DataError(f"no data returned for {symbol} {timeframe} {start}..{end}")
    df = pd.DataFrame(rows, columns=["ts", *COLUMNS]).drop_duplicates("ts")
    now_ms = client.milliseconds()
    step_ms = client.parse_timeframe(timeframe) * 1000
    df = df[df.ts + step_ms <= now_ms]  # drop the still-open candle
    cache_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(cache, index=False)
    return load_csv(cache, allow_gaps=True)
