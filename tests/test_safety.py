"""Mechanical guard: this kit must never be able to send orders or hold keys."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
FORBIDDEN = re.compile(
    r"create_order|cancel_order|privatePost|privateGet|set_leverage|fetch_balance"
    r"|apiKey|api_key|secret=|withdraw\("
)
SCANNED = {".py", ".md", ".toml", ".yml", ".yaml", ".json", ".sh"}
SKIP_DIRS = {".git", ".venv", ".superpowers", "__pycache__", ".pytest_cache", ".ruff_cache", ".cache"}


def _files():
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in SCANNED and not (SKIP_DIRS & set(p.relative_to(ROOT).parts)):
            if p.resolve() != SELF:
                yield p


def test_no_order_or_private_api():
    hits = []
    for p in _files():
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if FORBIDDEN.search(line):
                hits.append(f"{p.relative_to(ROOT)}:{i}: {line.strip()}")
    assert not hits, "Forbidden trading/private-API pattern found:\n" + "\n".join(hits)


def test_ccxt_only_public():
    offenders = [
        str(p.relative_to(ROOT))
        for p in _files()
        if p.suffix == ".py"
        and re.search(r"^\s*(import ccxt|from ccxt)|ccxt\.", p.read_text(encoding="utf-8"), re.M)
        and p.relative_to(ROOT).as_posix() != "src/rekit/data.py"
    ]
    assert not offenders, f"ccxt may only be used in src/rekit/data.py, found in: {offenders}"
