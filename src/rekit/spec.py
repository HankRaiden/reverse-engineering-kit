"""Hypothesis specification (TOML). Written in stage 5, locked after CHAIRMAN-GO."""
from __future__ import annotations

import importlib.util
import tomllib
from dataclasses import dataclass, field, fields
from math import prod
from pathlib import Path
from typing import Any

from .backtest import BacktestConfig
from .verdict import Criteria


class SpecError(ValueError):
    pass


@dataclass
class Hypothesis:
    id: str
    statement: str
    rule: str
    params: dict[str, Any]
    symbols: list[str]
    exchange: str
    timeframe: str
    start: str
    end: str
    criteria: Criteria
    backtest: BacktestConfig
    grid: dict[str, list] | None = None
    baseline_rule: str | None = None
    baseline_params: dict[str, Any] = field(default_factory=dict)
    allow_gaps: bool = False
    base_dir: Path = Path(".")

    @property
    def rule_files(self) -> list[Path]:
        refs = [self.rule] + ([self.baseline_rule] if self.baseline_rule else [])
        return sorted({(self.base_dir / r.partition(":")[0]).resolve() for r in refs})

    @property
    def n_variants(self) -> int:
        return prod(len(v) for v in self.grid.values()) if self.grid else 1

    def _load(self, ref: str):
        file, _, func = ref.partition(":")
        path = (self.base_dir / file).resolve()
        if not path.exists() or not func:
            raise SpecError(f"{self.id}: rule '{ref}' not found (expected 'file.py:function')")
        mod_spec = importlib.util.spec_from_file_location(f"rekit_rules_{path.stem}_{abs(hash(path))}", path)
        mod = importlib.util.module_from_spec(mod_spec)
        mod_spec.loader.exec_module(mod)
        if not hasattr(mod, func):
            raise SpecError(f"{self.id}: function '{func}' missing in {file}")
        return getattr(mod, func)

    @property
    def rule_fn(self):
        return self._load(self.rule)

    @property
    def baseline_fn(self):
        return self._load(self.baseline_rule) if self.baseline_rule else None


def _only(cls, d: dict, where: str) -> dict:
    allowed = {f.name for f in fields(cls)}
    unknown = set(d) - allowed
    if unknown:
        raise SpecError(f"{where}: unknown keys {sorted(unknown)} (allowed: {sorted(allowed)})")
    return d


def load_spec(path: str | Path) -> list[Hypothesis]:
    path = Path(path)
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    defaults = raw.get("defaults", {})
    out = []
    for h in raw.get("hypothesis", []):
        merged = {**defaults, **h}
        missing = [k for k in ("id", "statement", "rule", "symbols", "exchange", "timeframe", "start", "end")
                   if k not in merged]
        if missing:
            raise SpecError(f"hypothesis {merged.get('id', '?')}: missing {missing}")
        out.append(Hypothesis(
            id=merged["id"], statement=merged["statement"], rule=merged["rule"],
            params=merged.get("params", {}), symbols=list(merged["symbols"]), exchange=merged["exchange"],
            timeframe=merged["timeframe"], start=str(merged["start"]), end=str(merged["end"]),
            criteria=Criteria(**_only(Criteria, merged.get("criteria", {}), f"{merged['id']}.criteria")),
            backtest=BacktestConfig(**_only(BacktestConfig, merged.get("backtest", {}), f"{merged['id']}.backtest")),
            grid=merged.get("grid"), baseline_rule=merged.get("baseline_rule"),
            baseline_params=merged.get("baseline_params", {}),
            allow_gaps=bool(merged.get("allow_gaps", False)), base_dir=path.parent,
        ))
    if not out:
        raise SpecError("no [[hypothesis]] entries")
    ids = [h.id for h in out]
    if len(set(ids)) != len(ids):
        raise SpecError(f"duplicate hypothesis ids: {ids}")
    return out
