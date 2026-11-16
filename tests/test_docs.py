import re
from pathlib import Path

from rekit.spec import load_spec

ROOT = Path(__file__).resolve().parents[1]
MONEY = re.compile(r"\d[\d.,]*\s?(USDT|USD|EUR|€|\$)(?![A-Za-z])")


def _texts():
    for top in ("docs", "templates", "examples"):
        for p in (ROOT / top).rglob("*"):
            if p.is_file() and p.suffix in {".md", ".toml", ".json"} and ".cache" not in p.parts:
                yield p
    yield from ROOT.glob("README*.md")
    yield ROOT / "SAFETY.md"


def test_no_money_amounts():
    hits = [f"{p.relative_to(ROOT)}: {m.group(0)}" for p in _texts() for m in MONEY.finditer(p.read_text())]
    assert not hits, hits


def test_independence_notice_in_readmes():
    assert "not affiliated with EmperorBTC" in (ROOT / "README.md").read_text()
    assert "nicht mit EmperorBTC verbunden" in (ROOT / "README.de.md").read_text()


def test_template_specs_load():
    for lang in ("en", "de"):
        hs = load_spec(ROOT / "templates" / lang / "hypotheses.toml")
        assert hs and all(h.criteria.min_trades >= 30 for h in hs)


def test_expected_templates_and_docs_exist():
    templates = ["source.md", "principle-card.md", "rules-spec.md", "codability-matrix.md", "preregistration.md",
                 "hypotheses.toml", "assignment.md", "review.md", "approval-log.schema.json",
                 "refutation-register.md", "paper-plan.md", "post-mortem.md", "weekly-review.md"]
    docs = ["quickstart.md", "methodology.md", "organisation.md", "anti-patterns.md", "lessons-from-live.md",
            "transferability.md", "after-paper-trading.md", "glossary.md"]
    for lang in ("en", "de"):
        for t in templates:
            assert (ROOT / "templates" / lang / t).is_file(), f"templates/{lang}/{t}"
        for d in docs:
            assert (ROOT / "docs" / lang / d).is_file(), f"docs/{lang}/{d}"


DISCLAIMER_EN = "I accept no responsibility for any results"
DISCLAIMER_DE = "Ich übernehme keine Verantwortung für jegliche Ergebnisse"


def test_disclaimer_is_prominent_in_both_languages():
    d = (ROOT / "DISCLAIMER.md").read_text()
    assert DISCLAIMER_EN in d and DISCLAIMER_DE in d
    en, de = (ROOT / "README.md").read_text(), (ROOT / "README.de.md").read_text()
    assert DISCLAIMER_EN in en and DISCLAIMER_DE in de
    # prominent = before the first second-level heading
    assert en.index(DISCLAIMER_EN) < en.index("\n## ")
    assert de.index(DISCLAIMER_DE) < de.index("\n## ")
