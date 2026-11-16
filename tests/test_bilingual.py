"""Every doc and template must exist in English and German."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _rel(base: Path) -> set[str]:
    return {p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}


def test_every_doc_has_both_languages():
    for top in ("docs", "templates"):
        en, de = _rel(ROOT / top / "en"), _rel(ROOT / top / "de")
        assert en == de, f"{top}: only in en: {sorted(en - de)}; only in de: {sorted(de - en)}"
