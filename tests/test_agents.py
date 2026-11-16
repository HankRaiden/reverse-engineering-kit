import re
from pathlib import Path

from rekit.cli import COMMANDS, build_parser

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ["source", "principles", "rules", "codability", "preregister", "backtest", "refute", "paper-plan",
          "assignment", "review", "chairman"]
AGENTS = ["cio", "cto", "challenger"]


def _frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert m, "missing frontmatter"
    return dict(line.split(":", 1) for line in m.group(1).splitlines() if ":" in line)


def test_all_skills_exist_with_frontmatter():
    for s in SKILLS:
        fm = _frontmatter((ROOT / ".claude" / "skills" / s / "SKILL.md").read_text())
        assert fm["name"].strip() == s and fm["description"].strip()


def test_all_agents_exist_with_frontmatter():
    for a in AGENTS:
        fm = _frontmatter((ROOT / ".claude" / "agents" / f"{a}.md").read_text())
        assert fm["name"].strip() == a and fm["description"].strip()


def test_referenced_templates_and_commands_exist():
    subcommands = set(build_parser()._subparsers._group_actions[0].choices)
    assert subcommands == set(COMMANDS)
    files = [*(ROOT / ".claude").rglob("*.md"), ROOT / "AGENTS.md"]
    for f in files:
        text = f.read_text()
        for name in re.findall(r"templates/(?:<lang>|en|de)/([\w.-]+)", text):
            for lang in ("en", "de"):
                assert (ROOT / "templates" / lang / name).is_file(), f"{f.name} references missing {name}"
        for cmd in re.findall(r"rekit ([a-z-]+)", text):
            assert cmd in subcommands, f"{f.name} references unknown command 'rekit {cmd}'"


def test_gates_require_chairman_go():
    for s in ("chairman", "preregister", "paper-plan", "principles"):
        assert "CHAIRMAN-GO" in (ROOT / ".claude" / "skills" / s / "SKILL.md").read_text()


def test_constitution_forbids_orders_and_requires_rekit():
    text = (ROOT / "AGENTS.md").read_text()
    assert "never" in text.lower() and "orders" in text.lower()
    assert "rekit" in text
    assert "AGENTS.md" in (ROOT / "CLAUDE.md").read_text()
