"""Core functions for a defensive file-integrity monitor."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, List

DEFAULT_IGNORES = {".git", "__pycache__", ".venv", "venv"}


def sha256_file(path: Path, chunk_size: int = 65536) -> str:
    """Return the SHA-256 digest of a file without modifying it."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_baseline(directory: str) -> Dict[str, str]:
    """Create an in-memory hash baseline for regular files in directory."""
    root = Path(directory).resolve()
    if not root.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    baseline: Dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in DEFAULT_IGNORES for part in relative.parts):
            continue
        baseline[relative.as_posix()] = sha256_file(path)
    return baseline


def save_baseline(baseline: Dict[str, str], baseline_file: str) -> None:
    Path(baseline_file).write_text(
        json.dumps(baseline, indent=2, sort_keys=True), encoding="utf-8"
    )


def load_baseline(baseline_file: str) -> Dict[str, str]:
    path = Path(baseline_file)
    if not path.is_file():
        raise FileNotFoundError(f"Baseline file not found: {baseline_file}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in data.items()
    ):
        raise ValueError("Invalid baseline format")
    return data


def compare(directory: str, baseline: Dict[str, str]) -> Dict[str, List[str]]:
    """Compare current files with a baseline and report changes."""
    current = build_baseline(directory)
    old_names = set(baseline)
    new_names = set(current)

    added = sorted(new_names - old_names)
    deleted = sorted(old_names - new_names)
    modified = sorted(
        name for name in old_names & new_names if baseline[name] != current[name]
    )
    unchanged = sorted(
        name for name in old_names & new_names if baseline[name] == current[name]
    )
    return {
        "added": added,
        "modified": modified,
        "deleted": deleted,
        "unchanged": unchanged,
    }
