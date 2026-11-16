"""Mechanical guard: this kit must never be able to send orders or hold keys."""
import ast
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# files that must spell out the forbidden patterns in order to test the scanner itself
EXEMPT = {ROOT / "tests" / "test_safety.py", ROOT / "tests" / "test_review_fixes.py"}
PATTERNS = [
    re.compile(r"create_?order|cancel_?(all_?)?orders?|edit_?order|private_?(post|get|put|delete)"
               r"|fetch_?balance|set_?leverage|set_?margin|withdraw\s*\(|transfer\s*\(", re.I),
    re.compile(r"api_?key\s*[=:]|['\"]?\b(secret|apikey|api_key|password)\b['\"]?\s*[:=]", re.I),
    re.compile(r"__import__\(\s*['\"]ccxt|import_module\(\s*['\"]ccxt", re.I),
]
ALLOWED_CCXT_ATTRS = {"fetch_ohlcv", "milliseconds", "parse_timeframe", "load_markets", "iso8601", "parse8601"}
SCANNED = {".py", ".md", ".toml", ".yml", ".yaml", ".json", ".sh"}
SKIP_DIRS = {".git", ".venv", ".superpowers", "__pycache__", ".pytest_cache", ".ruff_cache", ".cache"}


def scan_text(text: str) -> list[str]:
    return [m.group(0) for p in PATTERNS for m in p.finditer(text)]


def _files():
    for p in ROOT.rglob("*"):
        if p.is_file() and p.suffix in SCANNED and not (SKIP_DIRS & set(p.relative_to(ROOT).parts)):
            if p.resolve() not in EXEMPT:
                yield p


def test_no_order_or_private_api():
    hits = []
    for p in _files():
        for i, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            for h in scan_text(line):
                hits.append(f"{p.relative_to(ROOT)}:{i}: {h}")
    assert not hits, "Forbidden trading/private-API pattern found:\n" + "\n".join(hits)


def test_ccxt_only_public():
    offenders = [
        str(p.relative_to(ROOT))
        for p in _files()
        if p.suffix == ".py"
        and re.search(r"^\s*(import ccxt|from ccxt)|ccxt\.", p.read_text(encoding="utf-8"), re.MULTILINE)
        and p.relative_to(ROOT).as_posix() != "src/rekit/data.py"
    ]
    assert not offenders, f"ccxt may only be used in src/rekit/data.py, found in: {offenders}"


def test_data_module_calls_only_public_methods():
    tree = ast.parse((ROOT / "src" / "rekit" / "data.py").read_text())
    calls = {n.func.attr for n in ast.walk(tree)
             if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
             and isinstance(n.func.value, ast.Name) and n.func.value.id == "client"}
    assert calls <= ALLOWED_CCXT_ATTRS, f"non-public exchange calls: {calls - ALLOWED_CCXT_ATTRS}"
