"""Pre-registration lock: after CHAIRMAN-GO the hypotheses file AND the rule code it uses are frozen (SHA-256)."""
from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path


class LockError(RuntimeError):
    pass


def _lock_path(path: Path) -> Path:
    return path.with_name(path.name + ".lock")


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _current(path: Path) -> dict[str, str]:
    from .spec import load_spec

    files = {path.name: _digest(path)}
    for h in load_spec(path):
        for f in h.rule_files:
            if not f.exists():
                raise LockError(f"rule file {f.name} referenced by {h.id} does not exist")
            files[f.relative_to(path.parent.resolve()).as_posix() if f.is_relative_to(path.parent.resolve())
                  else str(f)] = _digest(f)
    return files


def _read(lp: Path, spec_name: str) -> dict[str, str]:
    try:
        data = json.loads(lp.read_text())
    except (OSError, ValueError) as e:
        raise LockError(f"{lp.name} is unreadable ({e}); restore it from version control") from e
    if "files" in data:
        return data["files"]
    if "sha256" in data:  # first lock format: the hypotheses file only
        return {spec_name: data["sha256"]}
    raise LockError(f"{lp.name} has an unknown format")


def lock(path: str | Path) -> Path:
    path = Path(path)
    lp = _lock_path(path)
    files = _current(path)
    if lp.exists():
        old = _read(lp, path.name)
        if old == files:
            return lp
        same_registration = old.get(path.name) == files[path.name] and set(old) == {path.name}
        if not same_registration:
            raise LockError(f"{path.name} is already locked with different content. A lock is never replaced: "
                            "register a NEW hypotheses file (and count the extra trials).")
    lp.write_text(json.dumps({"files": files, "locked_at": datetime.now(UTC).isoformat(timespec="seconds")},
                             indent=2) + "\n")
    return lp


def verify_lock(path: str | Path) -> None:
    path = Path(path)
    lp = _lock_path(path)
    if not lp.exists():
        raise LockError(f"{path.name} is not locked. Pre-register first: get CHAIRMAN-GO, "
                        f"then run `rekit lock {path}`.")
    old = _read(lp, path.name)
    if old.get(path.name) != _digest(path):
        raise LockError(f"{path.name} changed after it was locked. Results would no longer be pre-registered. "
                        "Restore the locked version or register a NEW hypotheses file (and count the extra trials).")
    now = _current(path)
    for name, sha in old.items():
        if name != path.name and now.get(name) != sha:
            raise LockError(f"rule file {name} changed after {path.name} was locked. The test would no longer be "
                            "the one that was registered. Restore it or register a new hypotheses file.")
