"""Pre-registration lock: after CHAIRMAN-GO the hypotheses file is frozen by its SHA-256."""
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


def lock(path: str | Path) -> Path:
    path = Path(path)
    lp = _lock_path(path)
    lp.write_text(json.dumps({"file": path.name, "sha256": _digest(path),
                              "locked_at": datetime.now(UTC).isoformat(timespec="seconds")}, indent=2) + "\n")
    return lp


def verify_lock(path: str | Path) -> None:
    path = Path(path)
    lp = _lock_path(path)
    if not lp.exists():
        raise LockError(f"{path.name} is not locked. Pre-register first: get CHAIRMAN-GO, "
                        f"then run `rekit lock {path}`.")
    if json.loads(lp.read_text())["sha256"] != _digest(path):
        raise LockError(f"{path.name} changed after it was locked. Results would no longer be pre-registered. "
                        "Restore the locked version or register a NEW hypotheses file (and count the extra trials).")
