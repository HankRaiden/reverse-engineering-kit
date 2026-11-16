"""rekit command line. The agents call these commands instead of writing their own statistics."""
from __future__ import annotations

import argparse
import re
import sys
import time
from datetime import UTC, datetime
from itertools import product
from pathlib import Path

import pandas as pd

from . import __version__
from .backtest import run_backtest
from .data import DataError, fetch_public_ohlcv, load_csv
from .lock import LockError, lock, verify_lock
from .lookahead import LookAheadError, assert_no_lookahead
from .metrics import result_from_trades, summarize
from .paper import PaperTrader
from .report import write_report
from .spec import Hypothesis, SpecError, load_spec
from .stats import concentration, holm
from .verdict import verdict
from .walkforward import walk_forward

COMMANDS = ("fetch", "check-lookahead", "lock", "backtest", "paper")


def _safe(symbol: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", symbol).strip("-")


def _data(h: Hypothesis, symbol: str, csv_dir: Path | None, cache_dir: Path) -> pd.DataFrame:
    if csv_dir is not None:
        return load_csv(Path(csv_dir) / f"{_safe(symbol)}_{h.timeframe}.csv", allow_gaps=True)
    return fetch_public_ohlcv(h.exchange, symbol, h.timeframe, h.start, h.end, cache_dir)


def _bound(fn, params):
    return lambda d: fn(d, **params)


def _check_rules(h: Hypothesis, df: pd.DataFrame) -> None:
    variants = [{}] if not h.grid else [dict(zip(h.grid, v, strict=True)) for v in product(*h.grid.values())]
    for p in variants:
        assert_no_lookahead(_bound(h.rule_fn, {**h.params, **p}), df)
    if h.baseline_fn:
        assert_no_lookahead(_bound(h.baseline_fn, h.baseline_params), df)


def _trades(h: Hypothesis, fn, params, frames: dict[str, pd.DataFrame], use_grid: bool) -> pd.DataFrame:
    """All trades of one rule over all symbols. With a grid, only walk-forward out-of-sample trades count."""
    parts = []
    for sym, df in frames.items():
        if use_grid:
            factory = lambda **g: _bound(fn, {**params, **g})  # noqa: E731
            tr = walk_forward(df, factory, h.grid, h.backtest)["oos_trades"]
        else:
            tr = run_backtest(df, _bound(fn, params)(df), h.backtest, symbol=sym).trades
        parts.append(tr.assign(symbol=sym))
    return pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()


def cmd_backtest(args) -> int:
    spec = Path(args.spec)
    verify_lock(spec)
    hyps = load_spec(spec)
    cache = spec.parent / ".cache"
    n_trials = sum(h.n_variants for h in hyps)
    out = []
    for h in hyps:
        frames = {s: _data(h, s, args.csv_dir, cache) for s in h.symbols}
        _check_rules(h, next(iter(frames.values())))
        trades = _trades(h, h.rule_fn, h.params, frames, use_grid=bool(h.grid))
        base = _trades(h, h.baseline_fn, h.baseline_params, frames, use_grid=False) if h.baseline_fn else None
        res = result_from_trades(trades, h.backtest)
        v = verdict(trades["r_multiple"].to_numpy(), h.criteria, n_trials,
                    baseline_r=None if base is None else base["r_multiple"].to_numpy())
        out.append({"id": h.id, "statement": h.statement, "symbols": h.symbols, "timeframe": h.timeframe,
                    "period": f"{h.start} .. {h.end}", "out_of_sample": bool(h.grid),
                    "summary": summarize(res), "verdict": v,
                    "concentration": concentration(trades, 3) if len(trades) else {},
                    "concentration_by_symbol": concentration(trades, 1, by="symbol") if len(trades) else {}})
    ps = [o["verdict"]["p_value"] for o in out]
    testable = [i for i, p in enumerate(ps) if p == p]
    adj = holm([ps[i] for i in testable]) if testable else []
    for o in out:
        o["verdict"]["p_holm"] = float("nan")
    for i, a in zip(testable, adj, strict=True):
        v = out[i]["verdict"]
        v["p_holm"] = a
        if v["verdict"] == "ACCEPT" and a > out[i].get("alpha", 0.05):
            v["verdict"] = "REJECT"
            v["reason"] += f"; not significant after Holm correction across {len(testable)} hypotheses (p={a:.3f})"
    results = {"meta": {"spec": spec.name, "n_trials": n_trials, "rekit": __version__,
                        "created": datetime.now(UTC).strftime("%Y-%m-%d")}, "hypotheses": out}
    md = write_report(results, Path(args.out), lang=args.lang)
    print(f"report: {md}")
    for o in out:
        print(f"{o['id']}: {o['verdict']['verdict']} — {o['verdict']['reason']}")
    return 0


def cmd_check(args) -> int:
    spec = Path(args.spec)
    for h in load_spec(spec):
        df = _data(h, h.symbols[0], args.csv_dir, spec.parent / ".cache")
        _check_rules(h, df)
        print(f"{h.id}: no look-ahead detected")
    return 0


def cmd_lock(args) -> int:
    load_spec(args.spec)  # refuse to lock something that does not even parse
    print(f"locked: {lock(args.spec)}")
    return 0


def cmd_fetch(args) -> int:
    df = fetch_public_ohlcv(args.exchange, args.symbol, args.timeframe, args.start, args.end, Path(args.cache_dir))
    out = Path(args.cache_dir) / f"{_safe(args.symbol)}_{args.timeframe}.csv"
    df.reset_index().to_csv(out, index=False)
    print(f"{len(df)} candles -> {out}")
    return 0


def cmd_paper(args) -> int:
    spec = Path(args.spec)
    verify_lock(spec)
    h = next((x for x in load_spec(spec) if x.id == args.hypothesis), None)
    if h is None:
        raise SpecError(f"hypothesis {args.hypothesis} not in {spec.name}")
    symbol = args.symbol or h.symbols[0]
    journal = Path(args.journal or spec.parent / f"paper-{h.id}-{_safe(symbol)}.jsonl")
    trader = PaperTrader(_bound(h.rule_fn, h.params), h.backtest, journal, symbol)
    print(f"paper trading {h.id} on {symbol} ({h.timeframe}) — journal {journal}. No orders are ever sent.")
    while True:
        end = pd.Timestamp.now(tz="UTC")
        start = end - pd.Timedelta(h.timeframe.replace("m", "min")) * args.bars
        df = fetch_public_ohlcv(h.exchange, symbol, h.timeframe, start.isoformat(), end.isoformat(),
                                spec.parent / ".cache", use_cache=False)
        for e in trader.on_bar(df):
            print(e)
        if args.once:
            return 0
        time.sleep(args.poll_seconds)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="rekit", description="Reverse-engineering kit: test trading principles honestly.")
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="download public candles (no account, no key)")
    for a in ("--exchange", "--symbol", "--timeframe", "--start", "--end"):
        f.add_argument(a, required=True)
    f.add_argument("--cache-dir", default="work/data")
    f.set_defaults(fn=cmd_fetch)
    c = sub.add_parser("check-lookahead", help="prove the rules do not use future data")
    c.add_argument("spec")
    c.add_argument("--csv-dir", type=Path)
    c.set_defaults(fn=cmd_check)
    lk = sub.add_parser("lock", help="freeze the hypotheses file after CHAIRMAN-GO")
    lk.add_argument("spec")
    lk.set_defaults(fn=cmd_lock)
    b = sub.add_parser("backtest", help="run the pre-registered tests and write the report")
    b.add_argument("spec")
    b.add_argument("--out", default="work/06-backtest")
    b.add_argument("--csv-dir", type=Path)
    b.add_argument("--lang", choices=["en", "de"], default="en")
    b.set_defaults(fn=cmd_backtest)
    pp = sub.add_parser("paper", help="paper trade one hypothesis on live public candles (never sends orders)")
    pp.add_argument("spec")
    pp.add_argument("--hypothesis", required=True)
    pp.add_argument("--symbol")
    pp.add_argument("--journal")
    pp.add_argument("--bars", type=int, default=500)
    pp.add_argument("--poll-seconds", type=int, default=60)
    pp.add_argument("--once", action="store_true")
    pp.set_defaults(fn=cmd_paper)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except (LockError, LookAheadError, SpecError, DataError, FileNotFoundError) as e:
        print(f"rekit: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
